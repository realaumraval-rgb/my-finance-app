import streamlit as st
import yfinance as yf
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(layout="wide", page_title="Finance Hub")
st.title("🌌 Institutional Sentiment Hub")

ticker = st.text_input("Enter Ticker (e.g., AAPL)", "AAPL").upper()

if st.button("Fetch Live Data"):
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if news and len(news) > 0:
            df = pd.DataFrame(news)
            
            if 'title' in df.columns:
                sid = SentimentIntensityAnalyzer()
                df['Sentiment'] = df['title'].apply(lambda x: sid.polarity_scores(x)['compound'])
                st.metric("Average Sentiment", round(df['Sentiment'].mean(), 2))
                st.table(df[['title', 'Sentiment']])
            else:
                st.error("Data structure error: 'title' column not found.")
        else:
            st.error("No news found for this ticker.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
