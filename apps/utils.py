import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st


def calculate_returns(ds, periods=1):
    return ds.pct_change(periods=periods).dropna()

def calculate_log_returns(ds, periods=1):
    return np.log(ds / ds.shift(periods=periods)).dropna()

def obtain_stock_data_experimental(stock_list: list):
    ds = yf.download(' '.join(stock_list)).dropna()  # then you would want log returns but I've got a function for that
    return ds

def get_asx_ticker_symbols():   
    """Returns ticker symbols of ASX 200 companies (as of 27 February 2022)"""
    df = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200', match='Chairperson')[0]
    return df.set_index('Company').to_dict()['Code']
    
def app():
    st.write('Here are some useful functions included in many files in creating this app')
    code = """
import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

def calculate_returns(ds, periods=1):
    return ds.pct_change(periods=periods).dropna()

def calculate_log_returns(ds, periods=1):
    return np.log(ds / ds.shift(periods=periods)).dropna()

def obtain_stock_data_experimental(stock_list: list):
    ds = yf.download(' '.join(stock_list)).dropna()  # then you would want log returns but I've got a function for that
    return ds

def get_asx_ticker_symbols():   
    '''Returns ticker symbols of ASX 200 companies (as of 27 February 2022)'''
    df = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200', match='Chairperson')[0]
    return df.set_index('Company').to_dict()['Code']
"""
    
    st.code(code, language='python')