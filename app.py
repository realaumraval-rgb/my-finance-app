import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Custom CSS for the "Dashboard" look
st.markdown("""
    <style>
    .stMetric {background-color: #1c2029; padding: 20px; border-radius: 10px; border: 1px solid #333;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🌌 Institutional Hub")
    view = st.radio("Menu", ["Dashboard", "Analytics", "Settings"])
    st.markdown("---")
    st.write(f"System Time: {datetime.now().strftime('%H:%M:%S')}")

# Fixed Ticker List (No web scraping)
@st.cache_data
def get_tickers():
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "V", "JPM", "JNJ"]

tickers = get_tickers()

st.title("Dashboard")

# KPI Row
col1, col2, col3 = st.columns(3)
col1.metric("Market Sentiment", "Neutral", "0.0")
col2.metric("Assets Tracked", len(tickers), "0")
col3.metric("System Status", "Live", "OK")

# Analytics Area
st.subheader("Market Analytics")
df_demo = pd.DataFrame({'Time': range(10), 'Value': [0.1, 0.3, 0.2, 0.5, 0.4, 0.6, 0.8, 0.7, 0.9, 0.8]})
fig = px.area(df_demo, x='Time', y='Value', template='plotly_dark')
fig.update_traces(line_color='#FF8C00', fillcolor='rgba(255, 140, 0, 0.2)')
st.plotly_chart(fig, use_container_width=True)

# Selection & Data Grid
st.subheader("Asset Intelligence")
selection = st.selectbox("Select Asset to Analyze", tickers)

if st.button("Fetch Live Data"):
    stock = yf.Ticker(selection)
    news = stock.news
    if news:
        df = pd.DataFrame(news)
        sid = SentimentIntensityAnalyzer()
        df['Sentiment'] = df['title'].apply(lambda x: sid.polarity_scores(str(x))['compound'])
        st.dataframe(df[['title', 'Sentiment']], use_container_width=True)
    else:
        st.warning("No recent news found for this asset.")
