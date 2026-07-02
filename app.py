import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Custom CSS to mimic the polished dashboard look
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stMetric {background-color: #1c2029; padding: 20px; border-radius: 10px; border: 1px solid #333;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🌌 Institutional Hub")
    view = st.radio("Menu", ["Dashboard", "Analytics", "Settings"])
    st.markdown("---")
    st.write(f"Last update: {datetime.now().strftime('%H:%M:%S')}")

# Data Engine
@st.cache_data
def get_sp500():
    return pd.read_html('https://en.wikipedia.org/wiki/List_of_S&P_500_companies')[0]['Symbol'].tolist()

tickers = get_sp500()

st.title("Dashboard")
st.subheader("Market Strategy Performance")

# KPI Top Row (The "Product Overview" Style)
col1, col2, col3 = st.columns(3)
col1.metric("Avg Sentiment", "0.45", "+12%")
col2.metric("Total Active Assets", "500", "0%")
col3.metric("System Health", "Optimal", "100%")

# Main Analytics Area (Plotly "Abstract" look)
st.markdown("### Market Analytics")
df_demo = pd.DataFrame({'Time': range(20), 'Value': [0.1, 0.3, 0.2, 0.4, 0.5, 0.4, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.8]})
fig = px.area(df_demo, x='Time', y='Value', template='plotly_dark')
fig.update_traces(line_color='#FF8C00', fillcolor='rgba(255, 140, 0, 0.2)')
st.plotly_chart(fig, use_container_width=True)

# Bottom Data Grid
col4, col5 = st.columns([2, 1])
with col4:
    st.subheader("Top Performers")
    st.dataframe(pd.DataFrame({'Ticker': tickers[:10], 'Sentiment': [0.8, 0.7, 0.6, 0.9, 0.5, 0.4, 0.8, 0.7, 0.6, 0.9]}), use_container_width=True)
with col5:
    st.subheader("Quick Search")
    selection = st.selectbox("Search Company", tickers)
    if st.button("Generate Report"):
        st.write(f"Analyzing {selection}...")
