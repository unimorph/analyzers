# analyzers
Runnable Morphological Analysis Tools from the UniMorph Project

## Warning

This software is at an **alpha** stage. 

## Prerequisites

[DirecTL+](https://github.com/GarrettNicolai/DTL)

[CTranslate](https://github.com/OpenNMT/CTranslate)



## Installation

Uncompress DTL models into models/DTL directory. See **releases** tab above to download.

```
tar -xvzf DTLModel.tgz
```

Set environment variables to point to required binaries.

```
export DTL=<location of DTL binary>
export CTRANSLATE=<location of ctranslate binary>
```

## Usage

```
python src/analyze.py -i input.wordlist -a output.analyses -l language
```

For example:

```
python analyze.py -i Welsh.toAnalyze -a Welsh.out -l welsh
```


## Supported Languages

```
amharic, arabic, bengali, cornish, farsi, greenlandic, hindi, 
hungarian, indonesian, ingrian, karelian, kashubian, kazakh,
khakas, mapudungun, middle-high-german, middle-low-german, 
murrinhpatha, norman, romanian, russian, scottish-gaelic,
spanish, swahili, tagalog, tamil, tibetan, turkmen, welsh, 
west-frisian, zulu, ...
```
