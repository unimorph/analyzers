# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:39:57 2016

@author: christokirov
"""

import codecs
import re
import string
import sys


#read filenames from commandline
wordlistfile = sys.argv[1]
netoutputfile = sys.argv[2]
outputfile = sys.argv[3]


#load Tagalog feature lookup
scan2um = {}
fin = codecs.open('scan2unimorph.tsv','rb','utf-8')
for line in fin:
    parts = line.strip().split('\t')
    scan2um[parts[0]] = parts[1]
fin.close()

#load original input file
fin = codecs.open(wordlistfile,'rb','utf-8')
#read in network output file
fin2 = codecs.open(netoutputfile,'rb','utf-8')
#set up new output file
fout = codecs.open(outputfile,'wb','utf-8')

#postprocess
for line,line2 in zip(fin,fin2):
	inflection = line.strip()
	try:
		parts = line2.strip().split('|')
		lemma = parts[0].strip().replace(' ','').replace('_','')
		features = parts[1].strip().split()
		nufeatures = []
		for f in features:
			try:
				nufeatures.append(scan2um[f])
			except:
				pass
		nufeatures.append('V')
		if len(nufeatures) == 0:
			raise
		nufeatures = ';'.join(nufeatures)
		fout.write(inflection + '\t' + lemma + '\t' + nufeatures + '\n')
	except:
		fout.write(inflection + '\t' + 'MISS' + '\t' + 'MISS' + '\n')

#clean up
fin.close()
fin2.close
fout.close()



