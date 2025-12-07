<h1 align="center">📈 MOMENTUM TRADING BOT 🤖</h1>
<h4 align="center">An automated script designed to execute a configurable momentum-based trading strategy.</h4>

<div align="center">

| | | | |
| :---: | :---: | :---: | :---: |
| <img src="https://img.shields.io/badge/Strategy-Momentum%20Filter-blueviolet?style=for-the-badge" alt="Strategy Used"> | <img src="https://img.shields.io/badge/Python-3.8%2B-informational?style=for-the-badge&logo=python" alt="Python Version"> | <img src="https://img.shields.io/badge/Execution-Gemini%20CLI%20Subprocess-brightgreen?style=for-the-badge" alt="Execution Method"> | <img src="https://img.shields.io/github/license/google-gemini/gemini-cli?style=for-the-badge&label=License" alt="License"> |

</div>

---

<h2 align="center">✨ Key Features</h2>

This script provides a powerful and secure way to automate your trading logic directly from your system.

* **🚀 Strategy Implementation:** Uses a **Simple Moving Average (SMA) crossover** on historical data to generate clear BUY/SELL signals.
* **📊 Data Handling:** Leverages the **Pandas** library for efficient, fast processing and analysis of time-series financial data.
* **🔌 Secure Execution:** Executes trades by utilizing your configured **`gemini-cli`** via a subprocess call, keeping sensitive broker logic separate.
* **⏰ Scheduled Operation:** Designed for **single-run execution**, making it perfect for reliable scheduling with tools like `cron`.

---

<h2 align="center">📝 Getting Started</h2>

### 📦 Prerequisites

Before deployment, ensure you have the following installed and configured:

* **Python:** Version 3.8 or higher.
* **API Access:** Valid **Broker/Data Provider API Keys** (e.g., Alpaca) for fetching market data.
* **`gemini-cli`:** Must be installed and accessible in your system's PATH to execute trades.

### ⚙️ Installation

1.  **Clone the Repository:**
    bash
    git clone [https://github.com/google-gemini/gemini-cli.git](https://github.com/google-gemini/gemini-cli.git) 
    cd gemini-cli
    

2.  **Install Python Dependencies:**
    bash
    pip install pandas requests python-dotenv
    

### 🔑 Configuration

All sensitive keys and trading parameters should be stored as environment variables for security.

1.  **Create a `.env` file** in the project root:
    
    ALPACA_API_KEY="YOUR_KEY"
    ALPACA_SECRET_KEY="YOUR_SECRET"
    SMA_SHORT=50
    SMA_LONG=200
    SYMBOL="BTC/USD"
    

---

<h2 align="center">💡 Usage</h2>

### Running the Bot

Run the script directly to execute the entire sequence: fetch data, calculate the signal, and place an order if a cross is detected.

bash
python3 Momentum_bot.py
Automation
Set up a cron job on your server to run the script automatically at desired intervals (e.g., daily before market open).

<h2 align="center">🤝 Contribution</h2>

Contributions are welcome! If you have suggestions for new features, bug fixes, or strategy improvements, please follow these steps:

Fork the repository.

Create your feature branch (git checkout -b feature/NewIndicator).

Commit your changes (git commit -m 'Add new indicator calculation').

Push to the branch (git push origin feature/NewIndicator).

Open a Pull Request.

<h2 align="center">✉️ Contact & Connect</h2>

GitHub Profile: @careed23

Email: tat2creed@gmail.com

LinkedIn: Colten Reed

<h2 align="center">⚖️ License</h2>

Distributed under the MIT License. See LICENSE for more information.
