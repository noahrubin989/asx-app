import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import apps.utils as utils
import plotly.express as px
import plotly.graph_objs as go

    
def compute_bivariate_measures(log_returns, metric, stock_a, stock_b, window=60, plot=True):
    """
    Computes static and rolling correlation assuming you have a date index as well as two stocks' opening|closing|volumne etc.
    """
    window = min(window, log_returns.shape[0])
    if metric.lower() == 'correlation':
        metric_static = log_returns.corr().iloc[0, 1]
        metric_rolling = log_returns[stock_a].rolling(window=window).corr(log_returns[stock_b]).dropna()  # rolling window
    else: 
        metric_static = log_returns.cov().iloc[0, 1]
        metric_rolling = log_returns[stock_a].rolling(window=window).cov(log_returns[stock_b]).dropna()  # rolling window
    
    
    # Plotly prefers date to be just another pandas series rather than the index
    metric_rolling_as_df = metric_rolling.reset_index()
    metric_rolling_as_df.columns = ['Date', metric]
    
    if plot: 
        fig = px.line(metric_rolling_as_df, x="Date", y=metric)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        fig.update_layout(title_text=f'Rolling {metric} (Purple) & Static {metric} (Red)', title_x=0.5)
        fig.add_hline(y=metric_static, line=dict(color="red", width=1, dash="dot"))
        return fig
    else:
        return metric_static, metric_rolling  # as a series 
    

def app():
    st.title('Correlation and Covariance')
    st.write('This is the `Correlation and Covariance` page of the multi-page app where you can compute the rolling and static covariance and correlation of the log returns')
    
    company_info = utils.get_asx_ticker_symbols()
    stock1 = st.selectbox(label='Stock 1', options=company_info.keys())
    stock2 = st.selectbox(label='Stock 2', options=company_info.keys())
    
    if (stock1 and stock2) and (stock1==stock2):
        st.warning('Please compare different stocks')

    elif stock1 and stock2:
        # Collect the data (with some symbols it is dodgy (put a 'temporarily down' st.warning))
        stock1 = f"{company_info[stock1]}.AX"
        stock2 = f"{company_info[stock2]}.AX"
        stock_list = [stock1, stock2]
        
        data = yf.download(' '.join(stock_list), period='ytd').dropna()

        # Let the user select which column to analyse
        columns = np.unique([i[0] for i in data.columns]).tolist()
        selected_column = st.radio(label='Select the column to analyse', options=columns)
        data = data.xs(selected_column, axis='columns')
        
        log_returns = utils.calculate_log_returns(data)

        metric = st.radio(label='Select Option:', options=['Covariance', 'Correlation'])
        if metric:
            window = st.slider('Window Size', min_value=2, max_value=252, value=5, step=5)
            plot = compute_bivariate_measures(log_returns, metric, stock1, stock2, window=window, plot=True)
            st.plotly_chart(plot)
        
    
    
    