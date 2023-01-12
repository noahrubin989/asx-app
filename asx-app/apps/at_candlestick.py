import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import apps.utils as utils
import plotly.express as px
import plotly.graph_objs as go


def create_candlestick_plot(ds, selected_option, window_size_days=140, log_scale=False):
    """Candle stick chart with default SMA window as 20 weeks"""
    dataset = ds.copy()
    moving_average = f'SMA_{window_size_days}'
    dataset[moving_average] = dataset['Close'].rolling(window=window_size_days).mean()
    
    candlestick_plot = go.Candlestick(x=dataset.index, 
                                      open=dataset['Open'], 
                                      high=dataset['High'], 
                                      low=dataset['Low'], 
                                      close=dataset['Close'],
                                      name='Candlestick Plot')
    
    scatter_plot = go.Scatter(x=dataset.index, 
                              y=dataset[moving_average],
                              line=dict(color="#e0e0e0"),
                              name=f"Moving Average of {window_size_days} days")

    fig = go.Figure(data=[candlestick_plot])
    fig.add_trace(scatter_plot)

    title_settings = dict(text=f"{selected_option} Candle Stick Plot (Window of {window_size_days} Days)",
                          # x=0.5, 
                          # xanchor='center', 
                          y=0.9, 
                          yanchor='top')
    
    font_settings = dict(color='white')
    
    fig.update_layout(title=title_settings,
                      xaxis_rangeslider_visible=False, 
                      template='plotly_dark', 
                      xaxis_title='Date',
                      yaxis_title='Prices')
    if log_scale:
        fig.update_yaxes(type='log')  # good for crypto data
    return fig 

def app():
    st.title('Candlestick Chart')
    st.write('This is the `candlestick chart` page of the multi-page app')
    
    # If asx data:
    company_info = utils.get_asx_ticker_symbols()
    selected_option = st.selectbox(label='Choose A Stock', options=company_info.keys())
    data = yf.download(f'{company_info[selected_option]}.AX').dropna()
    
    window_size_days = st.slider(label='Enter Window Size (Days)', 
                                 min_value=1, 
                                 max_value=min(250, len(data)), 
                                 value=140, 
                                 step=1)
    
    fig = create_candlestick_plot(data, 
                                  selected_option, 
                                  window_size_days=window_size_days,
                                  log_scale=False)
    st.plotly_chart(fig)
    
    
    
        
    
    