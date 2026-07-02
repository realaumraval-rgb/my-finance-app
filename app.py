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
            
            # Extract the actual readable text from the raw dictionary/string mess
            # We look for 'title' or 'summary' and strip out the technical garbage
            def clean_text(x):
                if isinstance(x, dict): return x.get('title', '')
                return str(x)

            # We focus on the 'title' column if it exists, otherwise we clean the 'content'
            display_col = 'title' if 'title' in df.columns else 'content'
            
            # Perform Sentiment
            sid = SentimentIntensityAnalyzer()
            df['Sentiment'] = df[display_col].apply(lambda x: sid.polarity_scores(str(x))['compound'])
            
            # Display metrics
            st.metric("Average Market Mood", round(df['Sentiment'].mean(), 2))
            
            # Show only the clean headline and the score
            st.subheader("Latest Headlines")
            st.dataframe(df[[display_col, 'Sentiment']], use_container_width=True)
            
            # Add a simple chart
            st.subheader("Sentiment Distribution")
            st.bar_chart(df['Sentiment'])
            
        else:
            st.warning(f"No news found for {ticker}.")
            
    except Exception as e:
        st.error(f"Error processing data: {e}")
