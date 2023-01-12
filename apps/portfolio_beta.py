import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import apps.utils as utils
import statsmodels.api as sm
import plotly.express as px


def calculate_betas(log_returns, market_index):
    """Calculates betas. The reason why Y is a matrix and not a vector is so we don't need a for loop to regress y on x one by one"""
    X = log_returns[[market_index]]
    Y = log_returns.drop(columns=market_index)
    X_vals = sm.add_constant(X.values)
    Y_vals = Y.values
    beta = np.linalg.inv(X_vals.T @ X_vals) @ X_vals.T @ Y_vals
    return pd.Series(beta[1], Y.columns, name='Beta')


def plot_betas(betas):
    """Plots the pandas series of the betas"""
    betas = betas.sort_values()
    indexes = betas.index
    values = betas.values
    fig = px.bar(x=indexes, 
                 y=values,
                 color=values,
                 color_continuous_scale='teal',
                 labels={"x":"Company Name", "y":"Beta Value"})
    fig.update_coloraxes(colorbar_title_text="Beta Colour Mapping")
    fig.update_layout(title_text='Portfolio Betas', title_x=0.45)
    return fig
    
 
def app():
    st.title('Portfolio Beta')
    st.write("This is the `portfolio beta` page of the multi-page app.")
    company_info = utils.get_asx_ticker_symbols()
    chosen_companies = st.multiselect(label='We can compare the following stocks to the index: AXJO', options=company_info.keys())
    if chosen_companies:
        chosen_tickers = ['^AXJO'] + [f"{company_info[c]}.AX" for c in chosen_companies]
        
        # Only concerned about closing
        df = utils.obtain_stock_data_experimental(chosen_tickers)['Close']
        
        log_returns = utils.calculate_log_returns(df)

        min_date = log_returns.index.min().strftime("%d %B, %Y")
        max_date = log_returns.index.max().strftime("%d %B, %Y")
        st.write(f'Betas taken from data collected between {min_date} and {max_date}')
        
        betas = calculate_betas(log_returns, '^AXJO')  # if market == australian market or something
        betas.index = chosen_companies
        st.plotly_chart(plot_betas(betas))
