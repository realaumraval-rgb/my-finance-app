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
            
            # The "AI-Proof" fix: Check for 'title', then 'content', then 'summary'
            text_column = None
            for col in ['title', 'content', 'summary']:
                if col in df.columns:
                    text_column = col
                    break
            
            if text_column:
                sid = SentimentIntensityAnalyzer()
                # Apply sentiment to whichever column we found
                df['Sentiment'] = df[text_column].apply(lambda x: sid.polarity_scores(x)['compound'])
                st.metric("Average Sentiment", round(df['Sentiment'].mean(), 2))
                st.table(df[[text_column, 'Sentiment']])
            else:
                st.error(f"Could not find a text column to analyze. Columns found: {df.columns.tolist()}")
        else:
            st.warning(f"No news found for {ticker}.")
            
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
