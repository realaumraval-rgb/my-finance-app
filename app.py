import streamlit as st
import yfinance as yf
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(layout="wide", page_title="Finance Hub")

st.title("🌌 Institutional Sentiment Hub")
ticker = st.text_input("Enter Ticker (e.g., AAPL)", "AAPL").upper()

if st.button("Fetch Live Data"):
    stock = yf.Ticker(ticker)
    news = stock.news
    if news:
        df = pd.DataFrame(news)
        sid = SentimentIntensityAnalyzer()
        df['Sentiment'] = df['title'].apply(lambda x: sid.polarity_scores(x)['compound'])
        st.metric("Average Sentiment", round(df['Sentiment'].mean(), 2))
        st.table(df[['title', 'Sentiment']])
    else:
        st.error("No news found.")
