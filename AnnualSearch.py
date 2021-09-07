#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Hao Mai & Pascal Audet
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Created on Tue Sep  7 20:09:56 2021
Create Static Annual Earthquake Arrivals Catalogues
@author: Hao Mai

"""
# request modules
import time
import requests
import re
import pandas as pd
def query(year,which_half):
    starttime = time.time()
    # global station global region 365/2 days 
    URL = 'http://www.isc.ac.uk/cgi-bin/web-db-v4'
    # if it's too slow, try above mirror website
    # URL = 'http://isc-mirror.iris.washington.edu/iscbulletin/search/arrivals/'
    if which_half=="a":
        # first half of the year
        global_365 = {
                        'iscreview':'on',
                        'out_format':'CSV',
                        'ttime':'on',
                        'ttres':'on',
                        'tdef':'on',
                        'amps':'on',
                        'stnsearch':'GLOBAL',
                        'searchshape':'GLOBAL',
                        'start_year':str(year),
                        'start_month':'1',
                        'start_day':'1',
                        'start_time':'00:00:00',
                        'end_year':str(year),
                        'end_month':'6',
                        'end_day':'15',
                        'end_time':'23:59:59',
                        'req_mag_type':'Any',
                        'req_mag_agcy':'Any',
                        'include_links':'on',
                        'request':'STNARRIVALS'
        }
    # request target global events
    r = requests.get(url=URL, params = global_365)
    endtime = time.time()
    totaltime = endtime - starttime
    print("The running time of request is {0}min {1} sec".format(totaltime//60,totaltime%60))
    return r
def find_all_vars(text, *args):
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
    return recordings   



if __name__ == '__main__':
    years = [2007,2006,2005,2004,2003,2002,2001,2000]
    half = "a"
    for year in years:
        r = query(year,half)
        recordings = find_all_vars(r.text, 'EVENTID', 'STA','CHN',
                               'ISCPHASE','REPPHASE',  
                               'ARRIVAL_LAT', 'ARRIVAL_LON',
                               'ARRIVAL_ELEV','ARRIVAL_DIST','ARRIVAL_BAZ',
                               'ARRIVAL_DATE','ARRIVAL_TIME',
                               'ORIGIN_LAT' ,'ORIGIN_LON','ORIGINL_DEPTH',
                               'ORIGIN_DATE' ,'ORIGIN_TIME',
                               'EVENT_TYPE','EVENT_MAG')

        data = pd.DataFrame(data=recordings)
        filename = "./DataSet/" + "global_"+str(year)+"_365_"+half+".csv"
        data.to_csv(filename)     

