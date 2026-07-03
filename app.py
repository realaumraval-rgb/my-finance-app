import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# --- BACKEND: REAL-TIME FETCHING ---
@st.cache_data(ttl=60) # Cache for 60 seconds to prevent over-fetching
def get_live_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V", "JNJ"]
    data = []
    for t in tickers:
        stock = yf.Ticker(t)
        # Fetch live price change
        hist = stock.history(period="1d")
        if not hist.empty:
            change = ((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
            data.append({'Ticker': t, 'Change': change, 'Price': hist['Close'].iloc[-1]})
    return pd.DataFrame(data).sort_values(by='Change', ascending=False)

# --- UI LOGIC ---
st.session_state.last_refresh = datetime.now()
df = get_live_data()
seconds_ago = int((datetime.now() - st.session_state.last_refresh).total_seconds())

# Header Row: System Live & Refresh Timer
col1, col2 = st.columns([0.7, 0.3])
col1.title("Institutional Sentiment Hub")
col2.markdown(f"**🟢 System Live** | Updated {seconds_ago}s ago")

# Sidebar
with st.sidebar:
    st.subheader("Navigation")
    page = st.radio("View", ["Dashboard", "Settings"])
    st.markdown("---")
    if st.button("Manual Refresh"):
        st.cache_data.clear()
        st.rerun()

# Dashboard Content
if page == "Dashboard":
    m1, m2, m3 = st.columns(3)
    m1.metric("Market Sentiment", "Bullish", "+2.4%")
    m2.metric("Top Mover", f"{df.iloc[0]['Ticker']}", f"{df.iloc[0]['Change']:.2f}%")
    m3.metric("Assets Analyzed", len(df), "Live")

    st.subheader("Market Performance")
    fig = px.bar(df, x='Ticker', y='Change', color='Change', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Leaderboard")
    st.table(df)

elif page == "Settings":
    st.write("System configuration settings.")
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.rerun()
