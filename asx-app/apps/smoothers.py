import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tsa.api import Holt
import apps.utils as utils


def hodrick_prescott():
    pass

def single_exponential_smoothing(ds, column, span):
    """Performs single exponential smoothing, returning a dataframe that plotly can understand"""
    new_series = ds[column].ewm(span=span, adjust=False).mean()
    raw_data = {column: ds[column], "EWMA": new_series}
    results = pd.DataFrame(raw_data)
    results.reset_index(inplace=True)
    return results


def holt_exponential_smoothing(ds, column, exponential=True, alpha=0.1, beta=0.1):
    model = Holt(endog=ds[column], exponential=exponential, initialization_method='estimated')
    fit_model = model.fit(alpha, beta)
    
    new_series = fit_model.fittedvalues
    summary = fit_model.summary()
    
    if exponential:  
        raw_data = {column: ds[column], "Holt's Method (Multiplicative)": new_series}
    else: 
        raw_data = {column: ds[column], "Holt's Method (Additive)": new_series}
    
    results = pd.DataFrame(raw_data)
    results.reset_index(inplace=True)
    
    return results, summary
    

def plot_exponential_smoother(results):
    """Plots time series with many variables. note that date is not the index here"""
    fig = go.Figure()
    
    column_names = results.drop(columns='Date').columns
    colours = ['#008BDA', 'lime']
    for column, colour in zip(column_names, colours):
        scatter = go.Scatter(x=results.Date, y=results[column], line=dict(color=colour, width=1), name=column)
        fig.add_trace(scatter)
        
    # font dictionary: family="comic sans" is an option
    font_settings = dict(size=16, color="white")
    
    chosen_column = column_names[0]
    fig.update_layout(
        title=dict(text=f"{chosen_column} Series Exponential Smoothing", x=0.5, xanchor='center', y=0.9, yanchor='top'),
        template='plotly_dark',
        xaxis_title="Date",
        yaxis_title=chosen_column,
        legend_title="Series",
        xaxis_tickformat = '%B <br>%Y',
        font=dict(size=16, color="white")
    )
    
    fig.update_xaxes(rangeslider_visible=True)

    return fig
    
    
def app():
    st.title('Smoothing Techniques')
    st.write('This is the `data smoothing` page of the multi-page app.')
    
    company_info = utils.get_asx_ticker_symbols()
    selected_option = st.selectbox('Select an ASX stock', options=company_info.keys())
    data = yf.download(f'{company_info[selected_option]}.AX').dropna()

    radio_button = st.radio('Select an option', ['Single Exponential Smoothing', 'Holt Exponential Smoothing'])
    selected_column = st.radio(label='Select the column to analyse', options=data.columns)
    
    if radio_button == 'Single Exponential Smoothing':
        span = st.slider('Specify N-day Exponentially Weighted Moving Average', 
                         min_value=3, 
                         max_value=365,
                         step=1,
                         key=1)
        
        results = single_exponential_smoothing(data, selected_column, span)
        
    elif radio_button == 'Holt Exponential Smoothing':
        alpha = st.slider('Specify alpha', min_value=0.000001, max_value=0.999999, value=0.01)
        beta = st.slider('Specify beta', min_value=0.000001, max_value=0.999999, value=0.01)      
        
        trend_type = st.radio('Type of trend', ['Additive', 'Multiplicative'])
        if trend_type == 'Additive':
            results, summary = holt_exponential_smoothing(data, selected_column, exponential=False, alpha=alpha, beta=beta)
        else:
            results, summary = holt_exponential_smoothing(data, selected_column, exponential=True, alpha=alpha, beta=beta)
            
               
    p = plot_exponential_smoother(results)
    st.plotly_chart(p)
    
    checkbox = st.checkbox('Print Model Summary')
    if checkbox and radio_button == 'Single Exponential Smoothing':
        st.write(f"Single Exponential Smoothing: {span} day moving average")
    elif checkbox and radio_button == 'Holt Exponential Smoothing':
        st.write(summary)
    
    
    
  
        
