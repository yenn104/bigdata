# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 00:48:30 2023

@author: Yuta
"""

import pandas as pd
from dateutil.parser import parse
import datetime

#dọc file excel
df = pd.read_excel('D:/lby/Nam4/HKII/BIGDATA/LeThiBaoYen_0850080057/orginal.xlsx', sheet_name='Sheet1')

#Name
df['Name'] = df['Name'].str.replace(r"[^\w\s]","") 
df['Name'] = df['Name'].str.title()


#Note
df['Note'] = df['Note'].str.replace(r'\b\s+\b', ' ')
df['Note'] = df['Note'].str.strip()


#Phone
df['Phone']=df['Phone'].astype(str)
df['Phone'] = df['Phone'].apply(lambda x: x if x.startswith('84') else "84"+x)


#Birthday
for index, bd in df['Birthday'].items(): 
    try:
        date = parse(bd)
        date_obj = parse(date)
        df.loc[index, 'Birthday'] = date_obj.strftime('%Y-%m-%d')
        
    except:
        date_formats = ["%y%m%d","%d/%m/%Y", "%d-%m-%Y", "%Y%m%d", "%d/%m/%y", "%b-%d-%Y", "%Y/%m/%d", "%d%m%Y", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"]   
        for date_format in date_formats:
            try:
                dt = datetime.datetime.strptime(bd, date_format)
                df.loc[index, 'Birthday'] = dt.strftime("%Y-%m-%d")
                break
            except ValueError:
                pass

print(df)


df.to_excel('cleaning.xlsx'.format(date.today()), index=False)

