import pandas as pd
from datetime import datetime

def add_headers(df):
    ''' 
    add headers for raw OHLVC dataframe
    '''
    df.columns = ['UTC', 'Open', 'Highest', 'Lowest', 'Closing', 'Volume']

def add_isodate(df):
    '''
    add a column of ISO8601 datetime converted from UTC milliseconds
    '''
    iso_list = []
    for utc in df['UTC']:
        dt = datetime.fromtimestamp(utc/1000) #convert UTC milliseconds (int) to Datetime object
        iso = dt.replace(microsecond=0).isoformat()
        iso_list.append(iso)

    df.insert(1, 'ISO8601', iso_list, True)

def add_weekday(df):
    '''
    add a column of Weekdays (str)
    '''
    weekday_list = []
    for utc in df['UTC']:
        dt = datetime.fromtimestamp(utc/1000) #convert UTC milliseconds (int) to Datetime object
        weekday = dt.strftime('%A')
        weekday_list.append(weekday)
    
    df.insert(2, 'Weekday', weekday_list, True)

def add_hour(df):
    '''
    add a column of Hour
    '''
    hour_list = []
    for utc in df['UTC']:
        dt = datetime.fromtimestamp(utc/1000) #convert UTC milliseconds (int) to Datetime object
        hour = dt.hour
        hour_list.append(hour)
    
    df.insert(2, 'Hour', hour_list, True)

def formatdata(old_path, new_path, headers=True, isodate=True, weekday=False, hour=False):
    '''
    format data with specific requirements, and export to csv file
    '''
    df = pd.read_csv(old_path)

    if headers:
        add_headers(df)
    if isodate:
        add_isodate(df)
    if weekday:
        add_weekday(df)
    if hour:
        add_hour(df)
    
    df.to_csv(new_path, index=False)
    print(f'Formatted data saved to {new_path}')