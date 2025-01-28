# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 15:54:52 2023

@author: zil20
"""

import cryptocompare as cc
import pandas as pd
import datetime as dt
import numpy as np

def genesis_point(asset): 
    df = pd.DataFrame(cc.get_historical_price_day_all(asset, 'USD')).set_index('time')
    df.index = pd.to_datetime(df.index, unit = 's')
    first_date = pd.to_datetime(df[df['close'] != 0].index[0]).strftime("%m/%d/%Y")
    print('{}-USD pair daily price data start from {}.'.format(asset, first_date))
    print('')
    
def calculate_beta(): 
    pass 
    
def main():
    cc.cryptocompare._set_api_key_parameter('f0fad0667a7722525cb05cb38005a928ffe0092b8aaa980e802dabc3e689cb52')
    # Set up a list of assets
    assets = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 'AVAX', 'TRX', 'MATIC', 'LTC', 'CRO', 'BCH', 'LINK']
 
    '''
    for crypto in assets: 
        genesis_point(crypto)
    '''    
    
    #df0 is the master dataframe that contains all asset-USD cross daily close price. The first column is BTC.
    df0 = pd.DataFrame(cc.get_historical_price_day_all('BTC', 'USD')).set_index('time')
    df0.index = pd.to_datetime(df0.index, unit = 's')
    df0 = df0['close'].to_frame().rename(columns = {'close': 'BTC'})
    for asset in assets[1:]:
        df = pd.DataFrame(cc.get_historical_price_day_all(asset, 'USD')).set_index('time')
        df.index = pd.to_datetime(df.index, unit = 's')
        df0 = df0.join(df['close'].to_frame().rename(columns = {'close': asset}))
    df0 = df0.replace(0, np.nan)
    df_ret = df0.pct_change()
    
    start = dt.datetime(2020, 12, 31)
    end = dt.datetime(2022, 12, 31)
    df_ret_sub = df_ret[(df_ret.index >= start) & (df_ret.index <= end)]
    cov_mat = df_ret_sub.cov()
    beta = cov_mat.loc['BTC'] / cov_mat.loc['BTC', 'BTC']
    
    # 2021/12/31 - 2022/12/31
    #low_beta = ['TRX', 'BNB', 'XRP', 'BCH'] 
    #high_beta = ['MATIC', 'SOL', 'AVAX', 'ETH']
    
    # 2020/12/31 - 2022/12/31
    low_beta = ['TRX', 'ADA', 'XRP', 'BNB'] 
    high_beta = ['DOGE', 'MATIC', 'DOT', 'LINK']

    
    df_low = 1/4 * df_ret[low_beta].sum(axis = 1).to_frame('low beta')
    df_high = 1/4 * df_ret[high_beta].sum(axis = 1).to_frame('high beta')
    df_backtest = pd.concat([df_ret['BTC'].to_frame(), df_low, df_high], axis = 1)
    bt_start = dt.datetime(2023, 1, 1)
    df_backtest_sub = df_backtest[df_backtest.index >= bt_start]
    df_cumret = (1 + df_backtest_sub).cumprod()
    df_cumret.plot()


    

    
    
    
    (1+df_backtest_sub).cumprod().plot()
    
    
            
    

    #df = pd.DataFrame(cc.get_historical_price_day_all('LINK', 'USD')).set_index('time')
    #df.index = pd.to_datetime(df.index, unit = 's')
    #first_date = pd.to_datetime(df.index.values[0]).strftime("%m/%d/%Y")
    
    '''
    # CC BTC genesis date: 2010-07-17
    df = pd.DataFrame(cc.get_historical_price_day('BTC', 'USD', toTs = dt.datetime(2012,12,31))).set_index('time')
    df.index = pd.to_datetime(df.index, unit = 's')
    
    asset = 'ETH'
    currency = 'USD'
    df = pd.DataFrame(cc.get_historical_price_day('BTC', 'USD', allData = True)).set_index('time')
    df.index = pd.to_datetime(df.index, unit = 's')
    '''

if __name__ == '__main__': 
    main()