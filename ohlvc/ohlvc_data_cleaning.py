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

def formatdata(df):
    add_headers(df)
    add_isodate(df)
    add_weekday(df)
    # add_hour(df)

# -----------------------------------------------------------------------------
def main():
    df = pd.read_csv("ohlvc/binance.csv")
    formatdata(df)
    # print(df.head(10))
    # df.to_csv('daily_hour_volume/binance_daily_hour.csv', index=False)
    df.to_csv('daily_hour_volume/binance_daily_hour.csv', index=False)

if __name__ == "__main__":
    main()