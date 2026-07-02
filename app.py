import streamlit as st
import yfinance as yf
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Sidebar
with st.sidebar:
    st.title("Veselty Inc.")
    st.write("MAIN MENU")
    st.button("Dashboard")
    st.button("Analytics")

# Dashboard Header
st.title("Dashboard")
ticker = st.text_input("Enter Ticker", "AAPL").upper()

if st.button("Fetch Live Data"):
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if news and len(news) > 0:
            df = pd.DataFrame(news)
            
            # Find the first column that looks like text
            target_col = None
            for col in ['title', 'summary', 'content']:
                if col in df.columns:
                    target_col = col
                    break
            
            if target_col:
                sid = SentimentIntensityAnalyzer()
                df['Sentiment'] = df[target_col].apply(lambda x: sid.polarity_scores(str(x))['compound'])
                
                # KPIs (Top Row)
                col1, col2, col3 = st.columns(3)
                col1.metric("Avg Sentiment", round(df['Sentiment'].mean(), 2))
                col2.metric("Headlines Analyzed", len(df))
                col3.metric("Market Status", "Live")
                
                # Analytics Row
                st.subheader("Sentiment Distribution")
                st.area_chart(df['Sentiment'])
                
                # Details
                st.subheader("Latest Headlines")
                st.dataframe(df[[target_col, 'Sentiment']], use_container_width=True)
            else:
                st.error("Could not find any readable news headlines for this ticker.")
        else:
            st.warning("No news available for this ticker.")
    except Exception as e:
        st.error(f"App Error: {e}")
