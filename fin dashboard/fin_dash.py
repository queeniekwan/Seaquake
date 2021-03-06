import pandas as pd
import json
from datetime import datetime, timedelta

def clean_data(df):
    ''' filter and edit raw data into clean data '''
    # filter out rows where entry_trade_size_asset != exit_trade_size_asset; entry_trade_size_dollar = 0; exit_trade_size_dollar = 0
    df = df[df.entry_trade_size_asset == df.exit_trade_size_asset]
    df = df[df.entry_trade_size_dollar != 0]
    df = df[df.exit_trade_size_dollar != 0]
    
    # convert time columns to datetime object
    df['entry_trade_time_iso8601'] = pd.to_datetime(df['entry_trade_time_iso8601'])
    df['exit_trade_time_iso8601'] = pd.to_datetime(df['exit_trade_time_iso8601'])

    # add market_made_type
    df['market_made_type'] = df.apply(mm_condition, axis='columns')

    # add hold time (seconds)
    df['hold_time'] = df.exit_trade_time_unix - df.entry_trade_time_unix

    return df

def mm_condition(df):
    ''' apply condition for market_made_type '''
    if df.entry_trade_maker == True:
        if df.exit_trade_maker == True:
            return 'both sides maker'
        else:
            return 'entry maker'
    else:
        if df.exit_trade_maker == True:
            return 'exit maker'
        else:
            return 'both sides taker'

def create_fin_dash(df):
    ''' create and return the fin dashboard table with data from df '''
    
    # create table frame
    dash = pd.DataFrame(columns=['metric', 'value_type', 'total', 'today', 'yesterday', 'day-3', 'day-4', 'day-5', 'day-6', 'day-7', 'this_week', 'last_week', 'week-3', 'week-4', 'this_month', 'last_month'])
    
    dash.metric = ['trades', 'trade volume asset', 'trade volume dollar', 'spread profit', 'fee rebate', 'fee paid', 'net profit', 
                    'profitable trades', 'profitable trades', 'unprofitable trades', 'unprofitable trades',
                    'both sides maker', 'both sides maker', 'entry maker only', 'entry maker only', 'exit maker only', 'exit maker only', 'both sides taker', 'both sides taker',
                    'maker trade', 'maker trade', 'taker trade', 'taker trade',
                    'maker order', 'maker order', 'maker order volume', 'taker order', 'taker order', 'taker order volume', 
                    'long trade', 'long trade', 'short trade', 'short trade',
                    'entry limit order', 'entry limit order', 'entry market order', 'entry market order', 'exit limit order', 'exit limit order', 'exit market order', 'exit market order',
                    'avg order size asset', 'avg order size dollar', 'win trades avg hold time', 'lose trades avg hold time',
                    'timeframe', 'weekday']
    
    dash.value_type = ['value', 'value', 'value', 'value', 'value', 'value', 'value', 
                        'value', 'percentage', 'value', 'percentage', 
                        'value', 'percentage', 'value', 'percentage', 'value', 'percentage', 'value', 'percentage', 
                        'value', 'percentage', 'value', 'percentage', 
                        'value', 'percentage', 'value', 'value', 'percentage', 'value', 
                        'value', 'percentage', 'value', 'percentage', 
                        'value', 'percentage', 'value', 'percentage', 'value', 'percentage', 'value', 'percentage',
                        'value', 'value', 'value', 'value',
                        'str', 'str']
    
    # fill table columns
    # get utc today 00:00
    now = datetime.utcnow().strftime('%Y-%m-%d')
    today_start = datetime.strptime(now+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    
    # total
    dash.total = fill_findash_column(df)
    
    # loop fill today to day-7
    start = today_start
    end = None
    for column in dash[['today', 'yesterday', 'day-3', 'day-4', 'day-5', 'day-6', 'day-7']]: 
        dash[column] = fill_findash_column(df, start_date=start, end_date=end, col_type='day')
        end = start
        start -= timedelta(days=1)
    
    # loop fill this week to week-4
    wd_today = today_start.weekday() #weekday today (int, 0=Mon, 7=Sun)
    start = today_start - timedelta(days=wd_today)
    end = None
    for column in dash[['this_week', 'last_week', 'week-3', 'week-4']]:
        dash[column] = fill_findash_column(df, start_date=start, end_date=end, col_type='week')
        end = start
        start -= timedelta(weeks=1)
        
    # loop fill this month to last month
    start = today_start.replace(day=1)
    end = None
    for column in dash[['this_month', 'last_month']]:
        dash[column] = fill_findash_column(df, start_date=start, end_date=end, col_type='month')
        end = start
        last_day_prev_month = start - timedelta(days=1)
        start = last_day_prev_month.replace(day=1)

    return dash

def fill_findash_column(df, start_date=None, end_date=None, col_type=None):
    ''' return a list of data for a specific column in the fin_dash Dataframe from the df Dataframe
        df is the source data Dataframe, start_date and end_date filter data within this date range (default is None), col_type is type of this column (str: day, week, or month)
    '''
    # create a subset of data within the time range
    if start_date and end_date:
        data = df[(df.entry_trade_time_iso8601 >= start_date) & (df.entry_trade_time_iso8601 < end_date)]
    elif start_date:
        data = df[(df.entry_trade_time_iso8601 >= start_date)]
    else:
        data = df.copy()

    # date range and day of week
    if col_type == 'day':
        timeframe = start_date.strftime('%Y/%m/%d')
        wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = wd[start_date.weekday()]
    elif col_type == 'week':
        timeframe = start_date.strftime('%Y/%m/%d') + ' - ' + (start_date + timedelta(days=6)).strftime('%Y/%m/%d')
        weekday = 'N/A'
    elif col_type == 'month':
        timeframe = start_date.strftime('%Y/%m')
        weekday = 'N/A'
    else:
        timeframe = (data['entry_trade_time_iso8601'].min()).strftime('%Y/%m/%d') + ' - ' + (data['entry_trade_time_iso8601'].max()).strftime('%Y/%m/%d')
        weekday = 'N/A'
        
    # calculate value for each metric
    trades = data['id'].count()
    if trades == 0:
        column = ['N/A'] * 41 + [timeframe, weekday] + ['N/A'] * 4
    else:
        total_volume_asset = data['total_volume_asset'].sum()
        total_volume_dollar = data['total_volume_dollar'].sum()
        spread_profit = data['profit_dollar'].sum()
        fee_rebate = data['fee_rebate'].sum()
        fee_paid = data['fee_paid'].sum()
        net_profit = data['total_revenue'].sum()

        profitable = data[data['total_revenue']>0].count()['id']
        profitable_percent = profitable / trades
        unprofitable = data[data['total_revenue']<0].count()['id']
        unprofitable_percent = unprofitable / trades

        both_sides_maker = data[data['market_made_type']=='both sides maker'].count()['id']
        both_sides_maker_percent = both_sides_maker / trades
        entry_maker = data[data['market_made_type']=='entry maker'].count()['id']
        entry_maker_percent = entry_maker / trades
        exit_maker = data[data['market_made_type']=='exit maker'].count()['id']
        exit_maker_percent = exit_maker / trades
        both_sides_taker = data[data['market_made_type']=='both sides taker'].count()['id']
        both_sides_taker_percent = both_sides_taker / trades

        maker_trade = data[data['market_made_type']!='both sides taker'].count()['id']
        maker_trade_percent = maker_trade / trades
        taker_trade = both_sides_taker
        taker_trade_percent = both_sides_taker_percent

        maker_order = data[data['entry_trade_maker']==True].count()['id'] + data[data['exit_trade_maker']==True].count()['id']
        maker_order_percent = maker_order / (trades * 2)
        maker_order_volume = data[data['entry_trade_maker']==True].sum()['entry_trade_size_dollar'] + data[data['exit_trade_maker']==True].sum()['exit_trade_size_dollar']
        taker_order = data[data['entry_trade_maker']==False].count()['id'] + data[data['exit_trade_maker']==False].count()['id']
        taker_order_percent = taker_order / (trades * 2)
        taker_order_volume = data[data['entry_trade_maker']==False].sum()['entry_trade_size_dollar'] + data[data['exit_trade_maker']==False].sum()['exit_trade_size_dollar']

        long_trade = data[data['long']==True].count()['id']
        long_trade_percent = long_trade / trades
        short_trade = data[data['long']==False].count()['id']
        short_trade_percent = short_trade / trades

        entry_limit_order = data[data['entry_trade_order_type']=='LIMIT'].count()['id']
        entry_limit_order_percent = entry_limit_order / trades
        entry_market_order = data[data['entry_trade_order_type']=='MARKET'].count()['id']
        entry_market_order_percent = entry_market_order / trades
        exit_limit_order = data[data['exit_trade_order_type']=='LIMIT'].count()['id']
        exit_limit_order_percent = exit_limit_order / trades
        exit_market_order = data[data['exit_trade_order_type']=='MARKET'].count()['id']
        exit_market_order_percent = exit_market_order / trades

        avg_order_size_asset = data['entry_trade_size_asset'].mean()
        avg_order_size_dollar = data['total_volume_dollar'].mean() / 2
        win_trades_avg_hold_time = data[data['profit_dollar']>0].mean()['hold_time']
        lose_trades_avg_hold_time = data[data['profit_dollar']<0].mean()['hold_time']

        # put all values in a list
        column = [trades, total_volume_asset, total_volume_dollar, spread_profit, fee_rebate, fee_paid, net_profit, 
                    profitable, profitable_percent, unprofitable, unprofitable_percent,
                    both_sides_maker, both_sides_maker_percent, entry_maker, entry_maker_percent, exit_maker, exit_maker_percent, both_sides_taker, both_sides_taker_percent, 
                    maker_trade, maker_trade_percent, taker_trade, taker_trade_percent, 
                    maker_order, maker_order_percent, maker_order_volume, taker_order, taker_order_percent, taker_order_volume, 
                    long_trade, long_trade_percent, short_trade, short_trade_percent, 
                    entry_limit_order, entry_limit_order_percent, entry_market_order, entry_market_order_percent, exit_limit_order, exit_limit_order_percent, exit_market_order, exit_market_order_percent,
                    avg_order_size_asset, avg_order_size_dollar, win_trades_avg_hold_time, lose_trades_avg_hold_time,
                    timeframe, weekday]
        

    return column

def creat_mmlevel_dash(df):
    ''' create and return the mmlevel dashboard table with data from df '''
    dash = pd.DataFrame(columns=['position', 'mm_level', 
                                'total_trades', 'win_trades', 'win_rate', 'both_sides_maker', 'spread','rebate','fee_paid', 'revenue_per_level', 'win_trades_avg_holdtime_per_level', 'lose_trades_avg_holdtime_per_level',
                                'win_trades_avg_holdtime_per_side', 'lose_trades_avg_holdtime_per_side', 'revenue_per_side',
                                'total_revenue'])
    
    dash.position = ['long'] * 5 + ['short'] * 5
    dash.mm_level = [4, 3, 2, 1, 0, 0, 1, 2, 3, 4]

    # loop fill per level values
    for i in range(10):
        dash.loc[i] = fill_mmlevel_row(df, dash.loc[i].position, dash.loc[i].mm_level)
        # print(dash.loc[i])
    
    # calculate and fill per side value
    dash.win_trades_avg_holdtime_per_side.loc[dash.position == 'long'] = dash[dash.position == 'long'].mean()['win_trades_avg_holdtime_per_level']
    dash.win_trades_avg_holdtime_per_side.loc[dash.position == 'short'] = dash[dash.position == 'short'].mean()['win_trades_avg_holdtime_per_level']

    dash.lose_trades_avg_holdtime_per_side.loc[dash.position == 'long'] = dash[dash.position == 'long'].mean()['lose_trades_avg_holdtime_per_level']
    dash.lose_trades_avg_holdtime_per_side.loc[dash.position == 'short'] = dash[dash.position == 'short'].mean()['lose_trades_avg_holdtime_per_level']

    dash.revenue_per_side.loc[dash.position == 'long'] = dash[dash.position == 'long'].sum()['revenue_per_level']
    dash.revenue_per_side.loc[dash.position == 'short'] = dash[dash.position == 'short'].sum()['revenue_per_level']

    # calculate total revenue
    dash.total_revenue = dash['revenue_per_level'].sum()


    return dash

def fill_mmlevel_row(df, position, level):
    ''' return a list of data for a specific row in the mmlevel_dash Dataframe from the df Dataframe
        df is the source data Dataframe, position is str ('long' or 'short'), level is int (0 - 4)
    '''
    # create a subset of data with specific position and level 
    if position == 'long':
        data = df[(df.long == True) & (df.market_making_level == level)]
    else:
        data = df[(df.long == False) & (df.market_making_level == level)]


    # calculate value for each metric (column)
    total_trades = data.count()['id']
    if total_trades == 0:
        row = [0] * 10 + [''] * 4 
    else:
        win_trades = data[data.total_revenue > 0].count()['id']
        win_rate = win_trades / total_trades
        both_sides_maker = data[data.market_made_type == 'both sides maker'].count()['id']
        spread = data.profit_dollar.sum()
        rebates = data.fee_rebate.sum()
        fee_paid = data.fee_paid.sum()
        revenue_per_level = data.total_revenue.sum()
        win_trades_avg_holdtime_per_level = data[data.total_revenue > 0].mean()['hold_time']
        lose_trades_avg_holdtime_per_level = data[data.total_revenue < 0].mean()['hold_time']

        # put all values in a list
        row = [position, level, total_trades, win_trades, win_rate, both_sides_maker, spread, rebates, fee_paid, revenue_per_level, win_trades_avg_holdtime_per_level, lose_trades_avg_holdtime_per_level] + [''] * 4

    return row

def flip_position(df):
    ''' return df with flipped trades position (opposite 'long' and 'profit_dollar') '''
    
    for i, r in df.iterrows():
        df['long'][i] = not r['long']
        df['profit_dollar'][i] = - (r['profit_dollar'])

    return df

def trade_limit_analysis(df, parameter):
    ''' '''
    # create a subset of data with the specific parameter
    data = df[df.parameters == parameter]

    # calculate time range
    timerange = data.entry_trade_time_unix.max() - data.entry_trade_time_unix.min()
    period = timerange % 180

    # calculate metrics for each 3 min period
    start = data.entry_trade_time_unix.min()
    end = start + 180
    trade_limit = []
    for i in range(period):
        trade_count = data[(data['entry_trade_time_unix'] >= start) & (data['entry_trade_time_unix'] < end)].count()['id']
        start = end
        end += 180
        print(trade_count)
        trade_limit.append(trade_count)

    


def main():
    ''' open json input file and convert to df '''
    with open('fin dashboard/data.json') as f:
        data = json.load(f)
        df = pd.read_json(data)
    
    ''' process file and export dash to json '''
    df = clean_data(df)
    # df.to_csv('fin dashboard/clean_data.csv')
    # print(df.parameters.unique())

    # fin_dash = create_fin_dash(df)
    # dash.to_json('fin dashboard/fin_dash_data.json')
    # print(fin_dash)

    # mm_dash = creat_mmlevel_dash(df)
    # mm_dash.to_json('fin dashboard/mm_dash.json')
    # print(mm_dash)


    # flip = flip_position(df)
    # print(flip.long)

    trade_limit_analysis(df, 'bid-3-1-0.01-300-0.0003-5.0-0.0005-15-True')






if __name__ == "__main__":
    main()