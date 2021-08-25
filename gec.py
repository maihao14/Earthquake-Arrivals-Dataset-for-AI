#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 15:48:27 2021
Global Earthquake Catalog
@author: hao
"""

#%% import packages
from __future__ import (absolute_import, division, print_function)

# dependent packages
import os
import shutil
import logging
import csv
from obspy.core.utcdatetime import UTCDateTime
from obspy.clients.fdsn import Client
import warnings
import random
import numpy as np
import pandas as pd
import time
from scipy.io import savemat
LOGGER = logging.getLogger(__name__)
# terminal figure
import termplotlib as tpl
# regular expression
import re
# get arrival information from webpages
import requests
# command line progress
from progress.spinner import Spinner
from progress.bar import Bar
import matplotlib.pyplot as plt
# art font
from art import *
from obspy import read
import sys
#%% New QueryArrival
class QueryArrival():
    r"""Auto request online arrivals catalog
    This class fetch users's target arrivals from ISC Bulletin website.

    References
    ----------
    [1] International Seismological Centre (20XX), On-line Bulletin,
    https://doi.org/10.31905/D808B830

    """
    def __init__(self, **kwargs ):
        # ISC Bulletin url
        URL = 'http://www.isc.ac.uk/cgi-bin/web-db-v4'
        # init params dict
        self.param = {}
        self.starttime = time.time()
        # save params
        for k in kwargs:
            self.param[k] = kwargs[k]
        print("Loading time varies on your network connections, search region scale, time range, etc. Please be patient, estimated time: 3 mins ")
        try:
            
            self.response = requests.get(url = URL, params=self.param)
            self.page_text = self.response.text
        except:
            print("Error: No phase data was found. \n")
            return
                        
        if "No phase data was found." in self.page_text:
            print("Error: No phase data was found. \n")
            return("Please change your parameters and restart of the tool ... \n")

        try:
            self.find_all_vars(self.page_text, 'EVENTID', 'STA','CHN',
                               'ISCPHASE','REPPHASE', 
                               'ARRIVAL_LAT', 'ARRIVAL_LON',
                               'ARRIVAL_ELEV','ARRIVAL_DIST','ARRIVAL_BAZ',
                               'ARRIVAL_DATE','ARRIVAL_TIME',
                               'ORIGIN_LAT' ,'ORIGIN_LON','ORIGINL_DEPTH',
                               'ORIGIN_DATE' ,'ORIGIN_TIME',
                               'EVENT_TYPE','EVENT_MAG')
        except:
            print('Request failed. Data not available')
        else:
            print('Request completed！！！')
            print("%d events have been found!" % len(self.arrival_recordings))
            self.endtime = time.time()
            runtime = self.endtime - self.starttime
            if runtime > 60:
                min = runtime // 60
                sec = runtime % 60
                print("Query time is %d minutes %d seconds." % (min, sec))
            else:
                print("Query time is %d seconds." % (runtime))
            filename = "GSN_"+self.param['sta_list']+'_'+self.param['start_year']+'_'+self.param['min_mag']
            self.saverecord(filename)

    def saverecord(self, name):
        name = name + ".npy"
        np.save(name, self.arrival_recordings)                
    def find_all_vars(self, text, *args):
        r"""Store all arrival information
        This method save all fetched information into `recordings`:
            #. EVENTID
            #. STA
            #. PHASE NAME
            #. ARRIVAL DATE
            #. ARRIVAL TIME
            #. ORIGIN DATE
            #. ORIGIN TIME
            #. EVENT TYPE
            #. EVENT MAG
        """
        ex = r'MAG (.*) '
        all_variables = re.findall(ex, text, re.S)
        all_vars = re.split(r',', all_variables[0])
        #find last index
        for index in range(len(all_vars) - 1, 0, -1):
            if 'STOP' in all_vars[index]:
                break
        # initialization of recording, include all webset information
        recordings = {
        'EVENTID' : [] ,
        'STA' : [],
        'CHN' : [],
        'ISCPHASE' : [],
        'REPPHASE' : [],
        'ARRIVAL_LAT' : [],
        'ARRIVAL_LON' : [],
        'ARRIVAL_ELEV' : [],
        'ARRIVAL_DIST' : [],
        'ARRIVAL_BAZ' : [],
        'ARRIVAL_DATE' : [],
        'ARRIVAL_TIME' : [],
        'ORIGIN_LAT' : [],
        'ORIGIN_LON' : [],
        'ORIGINL_DEPTH' : [],
        'ORIGIN_DATE' : [],
        'ORIGIN_TIME' : [],
        'EVENT_TYPE' :[],
        'EVENT_MAG' : [] }
        pattern = re.compile(r'(?<=event_id=)\d*')
        pattern_sta = re.compile(r'stacode=(.*) target')
        for i in range(0, index, 25):
            recordings['EVENTID'].append(int(pattern.findall(all_vars[i])[0]))
            recordings['STA'].append(pattern_sta.findall(all_vars[i+2])[0])
            recordings['CHN'].append(str.strip(all_vars[i+6]))
            recordings['ISCPHASE'].append(str.strip(all_vars[i+9]))
            recordings['REPPHASE'].append(str.strip(all_vars[i+10]))
            recordings['ARRIVAL_LAT'].append(float(all_vars[i+3]))
            recordings['ARRIVAL_LON'].append(float(all_vars[i+4]))
            recordings['ARRIVAL_ELEV'].append(float(all_vars[i+5]))
            recordings['ARRIVAL_DIST'].append(float(all_vars[i+7]))
            recordings['ARRIVAL_BAZ'].append(float(all_vars[i+8]))
            recordings['ARRIVAL_DATE'].append(str.strip(all_vars[i+11]))
            recordings['ARRIVAL_TIME'].append(str.strip(all_vars[i+12]))
            recordings['ORIGIN_LAT'].append(float(all_vars[i+20]))
            recordings['ORIGIN_LON'].append(float(all_vars[i+21]))
            recordings['ORIGINL_DEPTH'].append(float(all_vars[i+22]))
            recordings['ORIGIN_DATE'].append(str.strip(all_vars[i+18]))
            recordings['ORIGIN_TIME'].append(str.strip(all_vars[i+19]))
            recordings['EVENT_TYPE'].append(str.strip(all_vars[i+24]))
            if str.isspace(re.split('\n', all_vars[i+25])[0]):
                recordings['EVENT_MAG'].append(float('NaN'))
            else:
                recordings['EVENT_MAG'].append(float(re.split('\n', all_vars[i+25])[0]))

        self.arrival_recordings = []
        for i in range(len(recordings['EVENTID'])):
            tempdict = {}
            for var in args:
                tempdict[var] = recordings[var][i]
            self.arrival_recordings.append(tempdict)
        return self.arrival_recordings
#%% find annual earthquakes catalog for each station
class EQCAT():
    def __init__(self, station):
        self.sta_pd = station
    def sta_cleaning(self):
        self.stalist = self.sta_pd['Station Code'].unique()
    def find_events_in_stalist(self):
        self.starttime = time.time()
        bar = Bar('Processing', max=len(self.stalist))
        for sta in self.stalist:
            # search 1990-2019
            #for year in np.arange(1990,2020):  
            year = '2009_2019'    
            params = self.set_params(sta,year)
            print("Station Name: {0}".format(sta))
            try:
                self.query = QueryArrival(**params)
            except KeyboardInterrupt:
                print("Stop at {0} in Station: {1}".format(year,sta))
                sys.exit()
            else:
                print("Earthquake Catalog in {0} for Station: {1} has completed!".format(year,sta))
            bar.next()  
        bar.finish()    
        self.endtime = time.time()
        self.runningtime = self.endtime- self.starttime
        print("Running time is {0}min, {1} sec".format(self.runningtime//60,self.runningtime%60))
    def set_params(self,sta,year):
        
        params= {
    #    """<output-format>"""
        'out_format':'CSV',  #<QuakeML>|<CSV>|<IMS1.0>
    #    """<request-type>"""
        'request':'STNARRIVALS', #Specifies that the ISC Bulletin should be searched for arrivals.
    #    """<arrivals-limits>"""
        'ttime':'on', # arrivals will be only be output if they have an arrival-time.
        'ttres':'on', #  they have a travel-time residual computed.
        'tdef':'on', # if they are time-defining phases.
        'iscreview':'on', # in the Reviewed ISC Bulletin
        'amps':'on',
    #    """station-region"""
        'stnsearch':'STN',  #<STN>|<GLOBAL>|<RECT>|<CIRC>|<FE>|<POLY>
        'sta_list':sta,
        'searchshape':'GLOBAL',
        'start_year':'2009',
        'start_month':'1',
        'start_day':'1',
        'start_time':'00:00:00',
        'end_year':'2019',
        'end_month':'12',
        'end_day':'31',
        'end_time':'23:59:59',
        'min_mag':'7.0',
        'req_mag_agcy':'Any',
        'req_mag_type':'Any',
        'include_links':'on'
        }      
        return params    
        
  

#%% main
def main():
    sta_pd = pd.read_csv('gsn.csv')
    gsn_cat = EQCAT(sta_pd[117:])  
    gsn_cat.sta_cleaning()
    gsn_cat.find_events_in_stalist()

#%% run functions
if __name__ == '__main__':
    main()