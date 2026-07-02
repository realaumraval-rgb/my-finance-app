import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Sidebar Menu (Matching "Main Menu" in Screenshot 2026-07-02 at 6.03.03 PM.jpg)
with st.sidebar:
    st.title("Veselty Inc.")
    st.menu = st.radio("MAIN MENU", ["Dashboard", "Products", "Orders", "Customers"])
    st.markdown("---")
    st.write("OTHER")
    st.write("📊 Analytics")
    st.write("⚙️ Settings")

# Dashboard Header
st.title("Dashboard")
st.write("Track your sentiment strategy performance")

ticker = st.text_input("Enter Ticker", "AAPL").upper()
if st.button("Fetch Live Data"):
    stock = yf.Ticker(ticker)
    news = stock.news
    df = pd.DataFrame(news)
    sid = SentimentIntensityAnalyzer()
    df['Sentiment'] = df['title'].apply(lambda x: sid.polarity_scores(str(x))['compound'])

    # Top KPI Row (Matching the "Product Overview/Active Sales" boxes)
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Sentiment", round(df['Sentiment'].mean(), 2), "1.2%")
    col2.metric("News Count", len(df), "5%")
    col3.metric("Volatility Index", "Low", "-2%")

    # Main Analytics Row (The "Main graph thingy" from Screenshot 2026-07-02 at 6.03.03 PM.jpg)
    st.subheader("Analytics")
    st.area_chart(df['Sentiment'])

    # Bottom Row (Top Products & Detailed view)
    col4, col5 = st.columns([2, 1])
    with col4:
        st.subheader("Sentiment Distribution")
        st.bar_chart(df['Sentiment'])
    with col5:
        st.subheader("Latest Headlines")
        st.dataframe(df[['title', 'Sentiment']], use_container_width=True)
