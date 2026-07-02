import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Page config
st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Initialize Session State for Navigation
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌌 Institutional Hub")
    if st.button("Dashboard"): st.session_state.page = "Dashboard"
    if st.button("Analytics"): st.session_state.page = "Analytics"
    if st.button("Settings"): st.session_state.page = "Settings"
    st.markdown("---")
    st.write(f"Refreshed: {datetime.now().strftime('%H:%M:%S')}")

# --- HEADER ROW ---
col_head1, col_head2 = st.columns([0.8, 0.2])
col_head1.title(f"{st.session_state.page}")
col_head2.markdown("<h3 style='text-align: right; color: #00FF00;'>● System Live</h3>", unsafe_allow_html=True)

# --- BACKEND LOGIC (FIXED) ---
@st.cache_data(ttl=300)
def fetch_top_movers():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "V", "JPM", "JNJ"]
    data = []
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            # Safe calculation: Try the standard key, or calculate from prices
            info = stock.fast_info
            price = info.get('last_price', 0)
            prev = info.get('previous_close', 0)
            
            # Calculate percentage change safely
            if prev > 0:
                change = ((price - prev) / prev) * 100
            else:
                change = 0.0
                
            data.append({'Ticker': t, 'Change': change})
        except:
            data.append({'Ticker': t, 'Change': 0.0})
            
    return pd.DataFrame(data).sort_values(by='Change', ascending=False)

# --- PAGES ---
if st.session_state.page == "Dashboard":
    movers = fetch_top_movers()
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Top Gainer", f"{movers.iloc[0]['Ticker']}", f"{movers.iloc[0]['Change']:.2f}%")
    m2.metric("Market Sentiment", "Bullish", "High Volatility")
    m3.metric("Assets Tracked", "10", "Live")
    
    # Graph
    st.subheader("Market Performance - Top 10")
    fig = px.bar(movers, x='Ticker', y='Change', color='Change', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top Movers Leaderboard")
    st.table(movers)

elif st.session_state.page == "Analytics":
    st.write("Detailed deep-dive analytics will go here.")
    st.info("Backend data pipelines are currently processing historical sentiment.")

elif st.session_state.page == "Settings":
    st.subheader("App Configuration")
    st.checkbox("Enable Dark Mode", value=True)
    if st.button("Clear Cache & Reboot"):
        st.cache_data.clear()
        st.rerun()
