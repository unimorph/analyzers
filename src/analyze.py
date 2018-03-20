# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 2018

@author: Garrett Nicolai

Morphological analyzer:
Usage:  python analyze.py -i inFile -o outFile -l language
inFile is the file to analyze
outFile is the location to print output
language is the language of the inFile

Languages currently supported: 

amharic
arabic
bengali
hindi
hungarian 
indonesian
persian
romanian
russian
spanish
swahili
tagalog
tamil
welsh

"""



import sys
import codecs
import re
import os
from optparse import OptionParser
from subprocess import call



#Get Options

parser = OptionParser()
parser.add_option("-i", "--in", dest="inFile",
                  help="FILE to analyze", metavar="FILE")
parser.add_option("-o", "--out", dest="outFile",
                  help="Write analyzed file to FILE", metavar="FILE")
parser.add_option("-l", "--lang", dest="language",
                  help="Language of file to be analyzed")
(options,args) = parser.parse_args()

if not options.inFile or not options.outFile or not options.language:
    parser.error("Usage must be python analyze.py -i inFile -o outFile -l language")



### Global variables ###

models = {}
lookup = {}
languages = []
orig2um = {}




modelIn = codecs.open("models.in", "r", "utf-8")
analyzedOutput = codecs.open("analyzed.out1", "w", "utf-8")
intermediateFile = codecs.open("toAnalyze.txt", "w", "utf-8")

#Read in parameters from model file


for i in modelIn:
    parts = i.split("\t")
    if(parts[0].lower() == options.language):
       models["Lookup"] = parts[1].strip()
       models["NN"] = parts[2].strip()
       models["DTL"] = parts[3].strip()
       models["Format"] = parts[4].strip()
    languages.append(parts[0])

modelIn.close()




if not models or models["Lookup"] == "NA":
   print("Sorry, that language is not yet supported. We currently support:" )
   for i in languages:
       print(i)
   print("More to come!")
   sys.exit()

#Determine conversion method for features

fConvert = ""

if(models["Format"] == "UD"):
    fConvert = codecs.open('../scripts/UD-UniMorph.tsv','rb','utf-8')
if(models["Format"] == "Tagalog"):
    fConvert = codecs.open('../scripts/scan2unimorph.tsv','rb','utf-8')

for line in fConvert:
    try:
        parts = line.strip().split('\t')
        orig2um[parts[0]] = parts[1]
    except:
        pass
try:
    fConvert.close()
except:
    pass


#Read lookup table into hash, converting if necessary
lookupIn = codecs.open(models["Lookup"], "r", "utf-8")

for line in lookupIn:
    parts = line.split("\t")
    sf = parts[0].strip()
    lemma = parts[1].strip()
    if(sf not in lookup):
       lookup[sf] = []
    features = parts[2].strip().split(";")
    nufeatures = []
    for f in features:
        try:
            if(sys.argv[4] != "UM"):
                nufeatures.append(orig2um[f])
            else:
                nufeatures.append(f)
        except:
            pass
    lookup[sf].append(lemma + "\t" + ";".join(nufeatures))
lookupIn.close()

analyzeIn = codecs.open(options.inFile, "r", "utf-8")


#Process inFile.  If instance is not in hash, then pass it to intermediate file

for line in analyzeIn:
    if line.strip() in lookup:
       analyses = lookup[line.strip()]
       for a in analyses:
           analyzedOutput.write(line.strip() + "\t" + a + "\n") 
    else:
       if(models["NN"] != "NA"):
           intermediateFile.write(" ".join(line.lower().strip().replace(" ", "_")) + " " + "\n")
       elif(models["DTL"] != "NA"):
           intermediateFile.write("#:" + ":".join(line.strip()).replace(" ", "!") + "@" + "\n") #DTL-specific format
       else:
           intermediateFile.write(line + "\n") #Catch-all


analyzeIn.close()
analyzedOutput.close()
intermediateFile.close()

#As long as there is an NN model, then we can analyze using the NN

if models["NN"] != "NA":
    try:
        call([os.environ["CTRANSLATE"], "--model", models["NN"], "--batch_size", "64", "--beam_size", "12", "--src", "toAnalyze.txt", "--tgt", "analyzed.nn.out"])
        if(models["Format"] == "UD"):
            call(["python", "../scripts/postprocessUDNetOutput.py", "toAnalyze.txt", "analyzed.nn.out", "analyzed.out2"])
	elif(models["Format"] == "UM"):
            call(["python", "../scripts/postprocessUMNetOutput.py", "toAnalyze.txt", "analyzed.nn.out", "analyzed.out2"])
	elif(models["Format"] == "Tagalog"):
            call(["python", "../scripts/postprocessTagalogNetOutput.py", "toAnalyze.txt", "analyzed.nn.out", "analyzed.out2"])
    
    except:
        print("There was an error.  You might want to disable the neural network")

#Otherwise, we backoff to DTL
elif models["DTL"] != "NA":  #Do DTL Analysis
    try:
        call([os.environ["DTL"], "--cs", "9", "--ng", "19", "--copy", "--jointMgram", "5", "--linearChain", "--order", "1", "--igNull", "--inChar", ":", "-t","toAnalyze.txt", "-a","analyzed.dtl.out", "--mi", models["DTL"]])     
        call(["python", "../scripts/postProcessDTL.py", "analyzed.dtl.out.phraseOut", "analyzed.out2", "c", models["Format"]])   
       
    except:
         print("There was an error.  Is DirecTL+ installed? If not, it can be obtained at ...")

#In the worst case, we skip the examples, and declare a miss
else:
    call("mv", "toAnalyze.txt", "analyzed.out2") 


#We now concatenate the lookup and analyzed forms back together.  Note, this will not follow the order of the original file.
filenames = ['analyzed.out1', 'analyzed.out2']
outFile = codecs.open(options.outFile, "w", "utf-8")    
for filename in filenames:
    inFile = codecs.open(filename, "r", "utf-8") 
    for line in inFile:
        parts = line.split("\t")
        if(len(parts) == 1):
            line = line + "\t" + "MISS"; #Unanalyzed, for cases where NN and DTL are unavailable, but lookup is available
        outFile.write(line)
    inFile.close()


#Cleanup

call(["rm", "-f", "toAnalyze.txt"])
call(["rm", "-f", "analyzed.out1"])
call(["rm", "-f", "analyzed.out2"])
call(["rm", "-f", "analyzed.nn.out"])
call(["rm", "-f", "analyzed.dtl.out.phraseOut"])
call(["rm", "-f", "analyzed.dtl.out"])

outFile.close()


