import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Page Configuration
st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# --- CUSTOM CSS FOR "VESELTY" LOOK ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {background-color: #1c2029; padding: 15px; border-radius: 10px; border: 1px solid #333;}
    .css-1r6slp0 {background-color: #0e1117;}
    .stApp {background-color: #0e1117;}
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC ---
@st.cache_data(ttl=300)
def get_dashboard_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"] # Limited to 5 for speed/relevance
    data = []
    sid = SentimentIntensityAnalyzer()
    
    for t in tickers:
        stock = yf.Ticker(t)
        # Get News Sentiment
        news = stock.news
        sentiment = 0
        if news:
            # Average the sentiment of the first 5 headlines
            sentiments = [sid.polarity_scores(n.get('title', ''))['compound'] for n in news[:5]]
            sentiment = sum(sentiments) / len(sentiments)
            
        data.append({'Ticker': t, 'Sentiment': sentiment})
        
    return pd.DataFrame(data)

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Dashboard"

with st.sidebar:
    st.title("🌌 Institutional Hub")
    if st.button("Dashboard"): st.session_state.page = "Dashboard"
    if st.button("Analytics"): st.session_state.page = "Analytics"
    st.markdown("---")
    st.write(f"Refreshed: {datetime.now().strftime('%H:%M:%S')}")

# --- DASHBOARD UI ---
st.title("Dashboard")
df = get_dashboard_data()

# KPI Row (The "Card" Style)
col1, col2, col3 = st.columns(3)
col1.metric("Market Mood", "Bullish" if df['Sentiment'].mean() > 0 else "Bearish", f"{df['Sentiment'].mean():.2f}")
col2.metric("Top Sentiment", df.loc[df['Sentiment'].idxmax()]['Ticker'], "High")
col3.metric("System Status", "Live", "Stable")

# Main Content Grid
st.subheader("Asset Sentiment Analysis")
fig = px.bar(df, x='Ticker', y='Sentiment', color='Sentiment', 
             color_continuous_scale='RdYlGn', template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sentiment Breakdown")
st.table(df.style.background_gradient(cmap='RdYlGn'))
