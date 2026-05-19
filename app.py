import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas_ta as ta

# Layout configuration
st.set_page_config(layout="wide")
st.title("Real-Time Stock Dashboard")

# Sidebar inputs
ticker = st.sidebar.text_input("Ticker Symbol", "AAPL")
period = st.sidebar.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "1y"])
chart_type = st.sidebar.selectbox("Chart Type", ["Candlestick", "Line"])
indicators = st.sidebar.multiselect("Indicators", ["SMA", "EMA"])

# Data fetching function [00:01:15]
def fetch_stock_data(ticker, period):
    # Mapping periods to intervals as suggested in the video [00:02:49]
    intervals = {"1d": "1m", "5d": "5m", "1mo": "1h", "3mo": "1d", "1y": "1d"}
    df = yf.download(ticker, period=period, interval=intervals[period])
    return df

# UI logic with Update button [00:03:05]
if st.sidebar.button("Update"):
    data = fetch_stock_data(ticker, period)
    
    # Technical Indicators calculation [00:02:03]
    if "SMA" in indicators:
        data['SMA'] = ta.sma(data['Close'], length=20)
    if "EMA" in indicators:
        data['EMA'] = ta.ema(data['Close'], length=20)

    # Metric Display [00:03:53]
    last_price = data['Close'].iloc[-1]
    st.metric("Current Price", f"{last_price:.2f}")

    # Plotting logic [00:04:28]
    fig = go.Figure()
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))
    else:
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines'))
    
    # Overlay Indicators [00:04:40]
    for ind in indicators:
        fig.add_trace(go.Scatter(x=data.index, y=data[ind], name=ind))
        
    st.plotly_chart(fig, use_container_width=True)
    