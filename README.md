# Earthquake-Arrivals-Dataset-for-AI
This repository provides various guides for building global scale earthquake arrivals catalogues and waveform datasets for AI use.

Author: [`Hao Mai`](https://www.uogeophysics.com/authors/mai/)(Developer and Maintainer)
 & [`Pascal Audet`](https://www.uogeophysics.com/authors/admin/) (Developer and Maintainer)

## Quick Start via Google Colab
Open `Google Colab` button to try the online version of the cookbook: ['Create Earthquake Catalog Introduction'](https://github.com/maihao14/Earthquake-Arrivals-Dataset-for-AI/blob/main/QuakeLabeler_with_Colab.ipynb)

## Local Installation
Download or clone the repository:
```bash
git clone https://github.com/maihao14/Earthquake-Arrivals-Dataset-for-AI.git
cd Earthquake-Arrivals-Dataset-for-AI
```

## Run scripts on shell
```bash
#mkdir DataSet
python AnnualSearch.py
```

## Finished arrival-based earthquake catalogues
Following the methods in above tutorial, we collected ISC reviewed arrival-based earthquake catalogues from 1980-2008. Storing in `CSV` format and recorded in each half year. After 2005, there are average 30,000 reviewed recordings in per half year. All documents are now available at [Google Drive](https://drive.google.com/drive/folders/1-4kHuYSwfNshdBsIdOsNkH5cPIgANOO5?usp=sharing).\\

We recommend to use `Pandas` to read and search for the data:

```
# Example
import pandas as pd
# read data from 01/01/2008 - 01/15/2008
cat_2008_a = pd.read_csv('global_2008_365_a.csv')
cat_2008_a.head()
```

Output:
You can use `pandas` operations to select the region and time range which you interest in. Next step we will apply `QuakeLabeler` to illustrate how to download the raw waveform and prepare for a final dataset.

```
EVENTID	STA	CHN	ISCPHASE	REPPHASE	ARRIVAL_LAT	ARRIVAL_LON	ARRIVAL_ELEV	ARRIVAL_DIST	ARRIVAL_BAZ	ARRIVAL_DATE	ARRIVAL_TIME	ORIGIN_LAT	ORIGIN_LON	ORIGINL_DEPTH	ORIGIN_DATE	ORIGIN_TIME	EVENT_TYPE	EVENT_MAG
13324982	BRTR	???	Pn	Pn	39.7250	33.6390	1440.0	2.72	322.8	2008-01-01	00:22:27.85	37.5771	35.7684	1.8	2008-01-01	00:21:42.02	mb	4.0
13324982	BRTR	???	Pg	Pg	39.7250	33.6390	1440.0	2.72	322.8	2008-01-01	00:22:33.50	37.5771	35.7684	1.8	2008-01-01	00:21:42.02	mb	4.0
13324982	MMAI	???	Pn	Pn	33.0153	35.4031	809.0	4.56	183.9	2008-01-01	00:22:51.87	37.5771	35.7684	1.8	2008-01-01	00:21:42.02	mb	4.0
13324982	MMAI	???	Sn	Sn	33.0153	35.4031	809.0	4.56	183.9	2008-01-01	00:23:43.92	37.5771	35.7684	1.8	2008-01-01	00:21:42.02	mb	4.0
13324982	ASF	???	Pn	Pn	32.1723	36.8972	937.0	5.47	169.9	2008-01-01	00:23:08.78	37.5771	35.7684	1.8	2008-01-01	00:21:42.02	mb	4.0
```








## Contributing

All constructive contributions are welcome, e.g. bug reports, discussions or suggestions for new features. You can either [open an issue on GitHub](https://github.com/maihao14/Earthquake-Arrivals-Dataset-for-AI/issues) or make a pull request with your proposed changes. Before making a pull request, check if there is a corresponding issue opened and reference it in the pull request. If there isn't one, it is recommended to open one with your rationale for the change. New functionality or significant changes to the code that alter its behavior should come with corresponding tests and documentation. If you are new to contributing, you can open a work-in-progress pull request and have it iteratively reviewed. Suggestions for improvements (speed, accuracy, etc.) are also welcome.
