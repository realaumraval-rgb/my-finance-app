import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Initialize Session State
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# --- BACKEND: REAL-TIME FETCHING ---
@st.cache_data(ttl=60)
def get_dashboard_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
    data = []
    sid = SentimentIntensityAnalyzer()
    
    for t in tickers:
        stock = yf.Ticker(t)
        # Price Change
        hist = stock.history(period="1d")
        change = ((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100 if not hist.empty else 0
        
        # Sentiment
        news = stock.news
        sentiment = 0
        if news:
            sentiments = [sid.polarity_scores(n.get('title', ''))['compound'] for n in news[:5]]
            sentiment = sum(sentiments) / len(sentiments)
            
        data.append({'Ticker': t, 'Change': change, 'Sentiment': sentiment})
    return pd.DataFrame(data)

# --- REFRESH LOGIC ---
df = get_dashboard_data()
seconds_ago = int((datetime.now() - st.session_state.last_refresh).total_seconds())

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌌 Institutional Hub")
    if st.button("Dashboard"): st.session_state.page = "Dashboard"
    if st.button("Analytics"): st.session_state.page = "Analytics"
    st.markdown("---")
    if st.button("Manual Refresh"):
        st.cache_data.clear()
        st.session_state.last_refresh = datetime.now()
        st.rerun()

# --- HEADER ROW ---
col1, col2 = st.columns([0.7, 0.3])
col1.title(f"{st.session_state.page}")
col2.markdown(f"**🟢 System Live** | Updated {seconds_ago}s ago")

# --- PAGE CONTENT ---
if st.session_state.page == "Dashboard":
    # KPIs
    m1, m2, m3 = st.columns(3)
    m1.metric("Market Sentiment", "Bullish" if df['Sentiment'].mean() > 0 else "Bearish", f"{df['Sentiment'].mean():.2f}")
    m2.metric("Assets Analyzed", len(df), "Live")
    m3.metric("System Status", "Stable", "OK")

    # Visualization
    st.subheader("Market Sentiment vs. Performance")
    fig = px.bar(df, x='Ticker', y='Sentiment', color='Sentiment', color_continuous_scale='RdYlGn', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    # Data Grid
    st.subheader("Asset Breakdown")
    # Using dataframe instead of table to avoid styling dependency errors if preferred, 
    # but with matplotlib added, this background_gradient will now work:
    st.table(df.style.background_gradient(cmap='RdYlGn'))

elif st.session_state.page == "Analytics":
    st.subheader("Deep Dive Analysis")
    st.write("Historical sentiment trends are loading...")
