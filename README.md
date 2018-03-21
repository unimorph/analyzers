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
amharic, arabic, bengali, farsi, hindi, 
hungarian, indonesian, romanian, russian, 
spanish, swahili, tagalog, tamil, welsh, 
zulu, ...
```
