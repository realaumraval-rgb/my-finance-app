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
        
        # Check if we actually got data back
        if news and len(news) > 0:
            df = pd.DataFrame(news)
            
            # Show the columns we found so we can see what's wrong if it fails
            if 'title' in df.columns:
                sid = SentimentIntensityAnalyzer()
                df['Sentiment'] = df['title'].apply(lambda x: sid.polarity_scores(x)['compound'])
                st.metric("Average Sentiment", round(df['Sentiment'].mean(), 2))
                st.table(df[['title', 'Sentiment']])
            else:
                st.error(f"Found news, but expected a 'title' column. Columns found: {df.columns.tolist()}")
        else:
            st.warning(f"No news found for {ticker}. Try a different ticker like 'AAPL', 'TSLA', or 'NVDA'.")
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
