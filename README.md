# Smelly London
_Mapping the history of London's smells_

The aim of the project is to use the dataset as a tool to explore and interpret the lives and health of the 19th and 20th century Londoners.

Data mine over 5500 Medical Officer of Health (MOH) reports from the Greater London area spanning from 1848 to 1972 and provide a historical interactive map of smells in London.

The health reports are available here:
http://wellcomelibrary.org/moh/

The project website is here:
http://londonsmells.co.uk/

Contributors: D. Leem, J. Thomas, C. Pina Estany, M. Robinson

## Setup

```
$ curl https://s3-eu-west-1.amazonaws.com/moh-reports/zips/Fulltext.zip -o Fulltext.zip
$ unzip Fulltext.zip
$ pip install nltk dataset
$ python -m nltk.downloader punkt
```

## Datamine smells

```
$ cd NLTK_textmine
$ python smell_datamine_multiprocessing.py
```