import os
import requests
import pandas as pd
import subprocess
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
SYMBOL = "BTC/USD"
TIMEFRAME = "5Min"
SMA_SHORT = 50
SMA_LONG = 100

# Load Keys (Variables are accessed inside functions for cleaner subprocess handling)
BASE_URL = "https://data.alpaca.markets/v1beta3/crypto/us/bars"

def get_historical_data():
    headers = {
        # Keys must be exported in the shell environment (e.g., in ~/env)
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY")
    }
    
    # --- FIX: Calculate Start Date for 5Min Timeframe ---
    # We request 48 hours (2 days) of data to ensure we have enough for the 200 period SMA.
    start_time = datetime.now() - timedelta(hours=48)
    start_time_rfc3339 = start_time.isoformat() + "Z" # Format correctly for API
    
    params = {
        "symbols": SYMBOL,
        "timeframe": TIMEFRAME,
        "start": start_time_rfc3339,
        "limit": 1000, 
        "sort": "desc" 
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        data = response.json()
        
        if "bars" in data and SYMBOL in data["bars"]:
            df = pd.DataFrame(data["bars"][SYMBOL])
            df["c"] = pd.to_numeric(df["c"])
            
            print(f"📡 Retrieved {len(df)} candles for {SYMBOL} ({TIMEFRAME})")
            
            # Since we requested 48 hours of data, we use the most recent 250 periods for the cross calculation
            df = df.tail(SMA_LONG + 50).reset_index(drop=True) 
            return df
        else:
            print(f"❌ Error: No data found. API Response: {data}")
            return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def calculate_signal(df):
    # Safety Check: We need at least 200 rows
    if len(df) < SMA_LONG:
        print(f"⚠️ Not enough data! Need {SMA_LONG} periods, but only got {len(df)}.")
        return "HOLD"

    # Calculate Moving Averages
    df['SMA_50'] = df['c'].rolling(window=SMA_SHORT).mean()
    df['SMA_100'] = df['c'].rolling(window=SMA_LONG).mean()
    
    # Get the last two completed candles (the critical crossover period)
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    current_price = last_row['c']
    
    print(f"📊 {SYMBOL} Price: ${current_price:.2f} | SMA 50: {last_row['SMA_50']:.2f} | SMA 100: {last_row['SMA_100']:.2f}")

    # Golden Cross Logic (Buy when 50 crosses ABOVE 00)
    if prev_row['SMA_50'] < prev_row['SMA_100'] and last_row['SMA_50'] > last_row['SMA_100']:
        return "BUY"
    # Death Cross Logic (Sell when 50 crosses BELOW 200)
    elif prev_row['SMA_50'] > prev_row['SMA_100'] and last_row['SMA_50'] < last_row['SMA_100']:
        return "SELL"
    else:
        return "HOLD"

def execute_trade_with_gemini(action):
    # Use a safe trailing distance, e.g., 2%
    TRAILING_PERCENT = "2%"
    
    print(f"🚀 SIGNAL DETECTED: {action}!")
    
    if action == "BUY":
        # Request the AI to place a complex order: Trailing Stop
        prompt = (f"Place a market order to buy 1 unit of {SYMBOL} and "
                  f"immediately attach a Trailing Stop Loss order with a trail "
                  f"distance of {TRAILING_PERCENT}."
        )
    elif action == "SELL":
        # On a Death Cross, we exit the position entirely (closing the long trade).
        prompt = f"Sell all my {SYMBOL} positions at market price (Trend Reversal Exit)."
    else:
        return

    try:
        # Calls Gemini CLI to execute the trade
        subprocess.run(
            ["gemini", "-p", prompt, "--yolo", "-m", "gemini-2.5-flash-lite"],
            check=True
        )
        print(f"✅ Trade sent: {action} order placed with {TRAILING_PERCENT} Trailing Stop.")
    except Exception as e:
        # This catches errors like failure to connect to the MCP server
        print(f"❌ Failed to execute trade via Gemini: {e}")

# --- SINGLE RUN EXECUTION ---
print("🛡️ Trend Following Bot Running (Single Execution)...")
df = get_historical_data()

if df is not None:
    signal = calculate_signal(df)
    if signal != "HOLD":
        execute_trade_with_gemini(signal)
    else:
        print("✋ No trade signal detected. Exiting.")
