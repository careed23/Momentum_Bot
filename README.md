<h1 align="center" style="font-size: 3em;">📈 Momentum Trading Bot</h1>
<h4 align="center">An automated script designed to execute momentum-based trading strategies.</h4>

---

## 🛡️ Project Status & Performance Badges

| Status | Badge | Description |
| :--- | :--- | :--- |
| **Strategy** | <img src="https://img.shields.io/badge/Strategy-Momentum%20Filter-blueviolet?style=for-the-badge" alt="Strategy Used"> | Indicates the core trading methodology (SMA Crossover). |
| **License** | <img src="https://img.shields.io/github/license/google-gemini/gemini-cli?style=for-the-badge&label=License" alt="License"> | Project license information. |
| **Dependencies** | <img src="https://img.shields.io/badge/Python-3.8%2B-informational?style=for-the-badge&logo=python" alt="Python Version"> | Required Python environment. |
| **Execution** | <img src="https://img.shields.io/badge/Execution-Gemini%20CLI%20Subprocess-brightgreen?style=for-the-badge" alt="Execution Method"> | How trade orders are handled. |

---

## ✨ Key Features

This bot is engineered for precision and speed, utilizing a classic trend-following momentum strategy.

* **🚀 Strategy Implementation:** Uses a configurable Simple Moving Average (SMA) crossover logic to generate BUY/SELL signals.
* **📊 Data Handling:** Uses `pandas` to efficiently fetch and analyze historical price data.
* **🔌 Trade Execution:** Integrates directly with your `gemini-cli` via `subprocess` for secure and fast order placement.
* **⏰ Scheduled Execution:** Designed for single-run execution, perfect for deployment using `cron` or other scheduling services.

---

## 📝 Getting Started

### 📦 Prerequisites

Ensure your environment is set up with the following:

* **Python:** Version 3.8 or higher.
* **API Access:** Valid Alpaca (or similar) API keys and secrets for data fetching.
* **`gemini-cli`:** Your custom command-line tool must be installed and configured in your system path.

### ⚙️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/google-gemini/gemini-cli.git](https://github.com/google-gemini/gemini-cli.git) # Adjust if your repo name is different
    cd gemini-cli
    ```

2.  **Install Dependencies:**
    ```bash
    pip install pandas requests python-dotenv
    ```

### 🔑 Configuration

Set your sensitive keys and trading parameters as environment variables for security.

1.  **Create a `.env` file** in the project root and add your keys:
    ```
    ALPACA_API_KEY="YOUR_KEY"
    ALPACA_SECRET_KEY="YOUR_SECRET"
    SMA_SHORT=50
    SMA_LONG=200
    SYMBOL="BTC/USD"
    ```

---

## 💡 Usage

### Running the Bot (Single Execution)

Execute the script directly to perform a single run, which fetches data, checks the current momentum signal, and executes a trade if a cross is detected.

```bash
python3 Momentum_bot.py
