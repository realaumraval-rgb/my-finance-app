import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="Institutional Sentiment Hub")

# Auto-refresh the page every 10 seconds (10000 milliseconds)
# This provides the "live" heartbeat you requested.
count = st_autorefresh(interval=10000, limit=None, key="data_refresh")

# --- BACKEND CACHING ---
# We cache this so we don't spam Yahoo Finance and get blocked.
@st.cache_data(ttl=60) # Refreshes data strictly every 60 seconds internally
def fetch_market_data(tickers):
    sid = SentimentIntensityAnalyzer()
    data = []
    
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            # 1. Price Data
            info = stock.fast_info
            price = info.get('lastPrice', 0.0)
            prev_close = info.get('previousClose', 0.0)
            change_pct = ((price - prev_close) / prev_close) * 100 if prev_close else 0.0
            
            # 2. News & Sentiment (-1.0 to 1.0)
            news = stock.news
            sentiment_score = 0.0
            if news:
                # Calculate compound score (-1 to 1) for recent headlines
                scores = [sid.polarity_scores(n.get('title', ''))['compound'] for n in news[:5]]
                sentiment_score = sum(scores) / len(scores) if scores else 0.0
                
            data.append({
                'Ticker': t, 
                'Price': price, 
                'Change (%)': change_pct, 
                'Sentiment (-1 to 1)': sentiment_score
            })
        except Exception:
            pass # Skip if API fails for a ticker to prevent crashing
            
    return pd.DataFrame(data)

@st.cache_data(ttl=3600) # Cache historical charts for an hour
def get_historical_chart(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'])])
    fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=30, b=0), height=300)
    return fig

# --- UI DASHBOARD ---
st.title("Institutional Sentiment Hub")
st.markdown(f"***Live Market Feed** | Last Ping: {datetime.now().strftime('%H:%M:%S')} (Updates 10s)*")

# Watchlist (Keep it small to prevent API rate limits)
watchlist = ["AAPL", "MSFT", "NVDA", "AMZN", "META"]
df = fetch_market_data(watchlist)

# --- KPI METRICS ---
if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    avg_sent = df['Sentiment (-1 to 1)'].mean()
    
    # Determine text based on score
    if avg_sent > 0.2: mood = "🟢 Bullish (Buy)"
    elif avg_sent < -0.2: mood = "🔴 Bearish (Sell)"
    else: mood = "⚪ Neutral (Hold)"

    col1.metric("Overall Market Mood", mood, f"Score: {avg_sent:.2f}")
    col2.metric("Top Performer", df.loc[df['Change (%)'].idxmax()]['Ticker'], f"{df['Change (%)'].max():.2f}%")
    col3.metric("Highest Sentiment", df.loc[df['Sentiment (-1 to 1)'].idxmax()]['Ticker'], f"{df['Sentiment (-1 to 1)'].max():.2f}")
    col4.metric("System Status", "Live", "Connected")

# --- VISUALIZATIONS ---
st.markdown("---")
col_chart, col_data = st.columns([2, 1])

with col_chart:
    st.subheader("Sentiment vs Price Movement")
    # A scatter plot showing how sentiment aligns with price changes
    fig = px.scatter(df, x='Sentiment (-1 to 1)', y='Change (%)', text='Ticker', 
                     color='Sentiment (-1 to 1)', color_continuous_scale='RdYlGn',
                     range_x=[-1.1, 1.1], template='plotly_dark')
    fig.update_traces(textposition='top center', marker=dict(size=15))
    # Add vertical/horizontal zero lines
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.add_vline(x=0, line_dash="dot", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("Live Scoring")
    # Display the dataframe with color gradients
    st.dataframe(df.style.background_gradient(subset=['Sentiment (-1 to 1)', 'Change (%)'], cmap='RdYlGn'), height=350)

# --- HISTORICAL DEEP DIVE ---
st.markdown("---")
st.subheader("Historical Asset Analysis")
selected_asset = st.selectbox("Select Asset to Analyze", watchlist)

tab1, tab2, tab3, tab4 = st.tabs(["1 Day", "1 Week", "1 Month", "1 Year"])
with tab1: st.plotly_chart(get_historical_chart(selected_asset, "1d"), use_container_width=True)
with tab2: st.plotly_chart(get_historical_chart(selected_asset, "5d"), use_container_width=True)
with tab3: st.plotly_chart(get_historical_chart(selected_asset, "1mo"), use_container_width=True)
with tab4: st.plotly_chart(get_historical_chart(selected_asset, "1y"), use_container_width=True)
