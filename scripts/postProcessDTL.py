import sys
import codecs
import re



fIn = codecs.open(sys.argv[1], "r", "utf-8")
fOut = codecs.open(sys.argv[2], "w", "utf-8")
affixing = sys.argv[3]

orig2um = {}
fConvert = ""

if(sys.argv[4] == "UD"):
    fConvert = codecs.open('UD-UniMorph.tsv','rb','utf-8')
if(sys.argv[4] == "Tagalog"):
    fConvert = codecs.open('scan2unimorph.tsv','rb','utf-8')

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


for i in fIn:
    if(i.strip() == ""):
        continue
    k = 0;
    i = i.strip()
    words = i.split("\t")
    surface = words[0]
    if(len(words) < 2):
        z = 0
    analysis = words[1]
    
    surfaceParts = surface.strip().split("|")
    analysisParts = analysis.strip().split("|")
#    z = 0;
    tag = ""
    lemma = ""
    stem = ""
    prefix = ""
    suffix = ""
    j = 0;
    deletion = ""
    while j < len(analysisParts):
        while "_" in analysisParts[j]:
            deletion += surfaceParts[j]
            j+= 1
        if "@" in surfaceParts[j] and (affixing == 'p' or affixing == 'c'):
            tag = analysisParts[j]
            prefix += surfaceParts[j]
            j += 1 
            continue    
            
        if "#" in surfaceParts[j] and (affixing == 's' or affixing == 'c'):
            tag = analysisParts[j]
            suffix += deletion
            deletion = ""
            suffix += surfaceParts[j]
            j += 1
            continue
        if ("@" in surfaceParts[j] and affixing == 's') or ("#" in surfaceParts[j] and affixing == 'p'):
            #lemma += analysisParts[j]
            #stem += surfaceParts[j]
            tag = analysisParts[j]
            stem += deletion
            deletion = ""
            j += 1
            continue
            
        if lemma == "" and (affixing == 'p' or affixing == 'c'):
            prefix += deletion
            deletion = ""
        else:
            stem += deletion
            deletion = ""
        lemma += analysisParts[j]
        stem += surfaceParts[j]
        j += 1
        
    tag = tag.replace("P*", "").replace("*","").replace("+","").replace("PREFIX","")
    features = tag.strip().split(";")
    nufeatures = []
    for f in features:
        try:
            if(sys.argv[4] != "UM"):
                nufeatures.append(orig2um[f])
            else:
                nufeatures.append(f)
        except:
            pass

    fOut.write(surface.strip().replace("@","").replace("#","").replace(":","").replace("|","") + "\t" + lemma + "\t" + ";".join(nufeatures) + "\n")
    

fIn.close();
fOut.close();

