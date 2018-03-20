# analyzers
Runnable Morphological Analysis Tools from the UniMorph Project

## Prerequisites

[DirecTL+](https://github.com/GarrettNicolai/DTL)

[CTranslate](https://github.com/OpenNMT/CTranslate)



## Installation

Uncompress DTL models into models/DTL directory.

```
tar -xvzf DTLmodels.tgz
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
arabic, hungarian, russian, romanian, hindi, swahili, welsh, ...
```
