import os
import requests
import pandas as pd
import subprocess
from datetime import datetime, timedelta

# --- CONFIGURATION (SCALPING) ---
SYMBOL = "BTC/USD"
TIMEFRAME = "1Min"  # Min feasible timeframe
VOLATILITY_THRESHOLD = 0.002 # 0.2% (as a decimal)

# Risk/Reward Settings (3:1 Ratio)
RISK_PERCENT = 0.002  # 0.2% Stop Loss
REWARD_PERCENT = 0.006 # 0.6% Take Profit (3x Risk)
TSL_PERCENT = 0.0005 # 0.05% trail to simulate granular 5-tick TSL

# Load Keys (Variables are accessed inside functions for cleaner subprocess handling)
BASE_URL = "https://data.alpaca.markets/v1beta3/crypto/us/bars"

def get_historical_data():
    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY")
    }
    
    # We only need the last 2 candles for a 1-minute check.
    start_time = datetime.now() - timedelta(minutes=5) # 5 minutes is a safe buffer
    start_time_rfc3339 = start_time.isoformat() + "Z"
    
    params = {
        "symbols": SYMBOL,
        "timeframe": TIMEFRAME,
        "start": start_time_rfc3339,
        "limit": 5, 
        "sort": "asc" 
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        data = response.json()
        
        if "bars" in data and SYMBOL in data["bars"]:
            df = pd.DataFrame(data["bars"][SYMBOL])
            df["c"] = pd.to_numeric(df["c"])
            
            print(f"📡 Retrieved {len(df)} candles for {SYMBOL} ({TIMEFRAME})")
            
            # Use the two most recent candles for analysis
            df = df.tail(2).reset_index(drop=True) 
            return df
        else:
            print(f"❌ Error: No data found. API Response: {data}")
            return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def calculate_signal(df):
    # Safety Check: We need exactly 2 rows for comparison
    if len(df) < 2:
        return "HOLD"

    current_close = df.iloc[-1]['c']
    prev_close = df.iloc[-2]['c']
    
    # Calculate the percentage change between the current and previous candle
    percent_change = (current_close - prev_close) / prev_close
    
    print(f"📊 {TIMEFRAME} Change: {percent_change*100:.3f}% (Threshold: {VOLATILITY_THRESHOLD*100:.2f}%)")

    if percent_change >= VOLATILITY_THRESHOLD:
        return "BUY"
    elif percent_change <= -VOLATILITY_THRESHOLD:
        return "SELL"
    else:
        return "HOLD"

def execute_trade_with_gemini(action):
    print(f"🚀 SIGNAL DETECTED: {action}!")
    
    # --- COMPLEX BRACKET ORDER LOGIC ---
    # We ask the AI to place a complex OCO/Bracket order with the required R:R and TSL.
    
    if action == "BUY":
        # The prompt is complex to enforce the R:R and TSL rules.
        prompt = (f"Place a Bracket Order to buy 1 unit of {SYMBOL}. "
                  f"Set the profit limit (take profit) to {REWARD_PERCENT*100:.2f}% "
                  f"(3x risk) and the stop loss to {RISK_PERCENT*100:.2f}%. "
                  f"Also, activate a trailing stop loss with a {TSL_PERCENT*100:.2f}% trail "
                  f"to act as a break-even stop, activated immediately."
        )
    elif action == "SELL":
        # For a short trade (selling first), the R:R is inverted.
        prompt = (f"Place a Bracket Order to sell 1 unit of {SYMBOL}. "
                  f"Set the profit limit to {REWARD_PERCENT*100:.2f}% and the stop loss to {RISK_PERCENT*100:.2f}%. "
                  f"Also, activate a trailing stop loss with a {TSL_PERCENT*100:.2f}% trail "
                  f"to act as a break-even stop, activated immediately."
        )
    else:
        return

    try:
        # Calls Gemini CLI to execute the trade
        subprocess.run(
            ["gemini", "-p", prompt, "--yolo", "-m", "gemini-2.5-flash-lite"],
            check=True
        )
        print(f"✅ Trade sent: {action} order placed with 3:1 R:R and Trailing Stop.")
    except Exception as e:
        print(f"❌ Failed to execute trade via Gemini: {e}")

# --- SINGLE RUN EXECUTION ---
print("🛡️ Volatility Scalping Bot Running (Single Execution)...")
df = get_historical_data()

if df is not None:
    signal = calculate_signal(df)
    if signal != "HOLD":
        execute_trade_with_gemini(signal)
    else:
        print("✋ No trade signal detected. Exiting.")
