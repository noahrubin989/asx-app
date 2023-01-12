import streamlit as st
from multiapp import MultiApp
from apps import (home, 
                  at_candlestick,
                  smoothers, 
                  portfolio_beta, 
                  correlation_covariance, 
                  utils, 
                  black_scholes)

app = MultiApp()

st.markdown("""
            # Finance App
            
            ### Created By: Noah Rubin
            📊 [LinkedIn](https://www.linkedin.com/in/noah-rubin1/)  
            
            🧑🏽‍💻 [GitHub](https://github.com/noahrubin989)
            """)

# Add all your applications here
app.add_app("Home", home.app)
app.add_app("Portfolio Beta", portfolio_beta.app)
app.add_app("Smoothing Techniques", smoothers.app)
app.add_app("Correlation & Covariance", correlation_covariance.app)
app.add_app('Candle Stick Plots', at_candlestick.app)
app.add_app("Black Scholes", black_scholes.app)
app.add_app("Utils", utils.app)



# The main app
app.run()
