# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 18:59:17 2022

@author: zil20
"""

import requests
import pandas as pd
import numpy_financial as npf
import numpy as np

def get_histo_prc(symbol, exchange, api_key, allData):
    api_url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym={exchange}&allData={allData}&api_key={api_key}'
    raw_data = requests.get(api_url).json()
    df = pd.DataFrame(raw_data['Data']['Data'])[['time', 'close']].set_index('time')
    df.index = pd.to_datetime(df.index, unit = 's')
    return df

def calculate_apy(daily_prcs, biz_days):
    daily_return = daily_prcs.pct_change(1)
    daily_return.replace([np.inf, -np.inf], np.nan, inplace=True)
    return daily_return.mean() * biz_days

def main(): 
    global res, i, magic_amt
    api_key = '22f31637367566b7fb665549bf27ead2b17add5df90328144d014444deabf8e3'
    symbol = 'BTC'
    #symbol = 'ETH'
    exchange = 'USD'
    allData = 'true'
    res = get_histo_prc(symbol, exchange, api_key, allData)
    
    business_days = 365
    i = calculate_apy(res, business_days)

    fv = 1000000
    yr = np.array([1, 2, 3, 4, 5])
    comp_fre = 12
    magic_amt = npf.pmt(i/comp_fre, yr*comp_fre, 0, fv)
    
    recurring_pmt = -100
    magic_fv = npf.fv(i/comp_fre, yr*comp_fre, recurring_pmt, 0)

    with np.printoptions(precision = 0, suppress = True):
        print(f'Using {symbol} to become millionaire in {yr} years: ')
        print(magic_amt)
        #print()
        #print(f'Investing {-recurring_pmt} per paycheck will compound in {yr} years to: ')
        #print(magic_fv)
    
    
if __name__ == '__main__':
    main()