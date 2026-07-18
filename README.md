# 📈 Live Stock & Crypto Dashboard

A real-time data analytics and visualization platform for monitoring stock market and cryptocurrency prices with advanced analytics and trading signals.
Live demo: https://stock-crypto-dashboard.streamlit.app/
## 🎯 Features

### Phase 1 (MVP)
- ✅ Real-time price feeds for stocks and cryptocurrencies
- ✅ Interactive candlestick charts with technical indicators
- ✅ Moving averages (SMA, EMA)
- ✅ Price alerts and buy/sell signals
- ✅ Portfolio tracker with P&L calculations
- ✅ Responsive web dashboard

### Phase 2 (Enhancement)
- 🔍 Sentiment analysis from financial news
- 🤖 Predictive analytics with ML models
- 👥 Multi-user support with authentication
- 📊 Historical trend analysis
- 📱 Mobile-responsive UI

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Data Source:** yfinance, Alpha Vantage API
- **Visualization:** Plotly, Altair
- **Database:** SQLite (for caching and historical data)
- **Real-time Updates:** WebSockets via Streamlit
- **Deployment:** Docker + Cloud (Render/Railway/Heroku)

## 📦 Project Structure

```
stock-crypto-dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main Streamlit app
│   ├── config.py               # Configuration settings
│   └── pages/
│       ├── dashboard.py        # Main dashboard
│       ├── portfolio.py        # Portfolio tracker
│       ├── analytics.py        # Technical analysis
│       └── alerts.py           # Price alerts
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py         # API data fetching
│   ├── technical_analysis.py   # Indicators: SMA, EMA, RSI, MACD
│   ├── database.py             # SQLite operations
│   └── utils.py                # Helper functions
├── data/
│   └── stock_crypto.db         # SQLite database
├── tests/
│   ├── __init__.py
│   ├── test_data_fetcher.py
│   └── test_analysis.py
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose for local dev
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KashishJainCS-a11y/stock-crypto-dashboard.git
   cd stock-crypto-dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys if needed
   ```

5. **Run the app**
   ```bash
   streamlit run app/main.py
   ```

   The app will open at `http://localhost:8501`

### Using Docker

```bash
docker-compose up
```

App will be available at `http://localhost:8501`

## 📚 API Keys

### Free APIs Used
- **yfinance** - No API key needed (built-in)
- **Alpha Vantage** - Get free API key at https://www.alphavantage.co/
- **CoinGecko** - No API key needed for basic usage

## 🎓 Learning Outcomes

By building this project, you'll learn:
- Real-time data fetching and processing
- Technical analysis and trading indicators
- Time-series data visualization
- Database design and operations
- Web dashboard development with Streamlit
- API integration
- Docker containerization
- Cloud deployment

## 📋 Project Roadmap

- [ ] Phase 1: MVP Dashboard
- [ ] Phase 2: Advanced Analytics
- [ ] Phase 3: ML Predictions
- [ ] Phase 4: Multi-user Auth
- [ ] Phase 5: Mobile App
- [ ] Phase 6: Production Deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit PRs.

## 📄 License

MIT License - see LICENSE file for details

## 💡 Tips

- Start with Phase 1 to get a working MVP
- Use free APIs to avoid costs
- Test with 5-10 stocks/cryptos first before scaling
- Use SQLite for caching to reduce API calls
- Deploy on Render or Railway for free tier

## 🔧 Troubleshooting

### API Rate Limits
- yfinance has rate limits; use caching
- Alpha Vantage free tier: 5 requests/min
- Add delays between requests

### Streamlit Issues
- Clear cache: `streamlit cache clear`
- Restart server if changes don't show

## 📧 Contact

For questions or suggestions, feel free to open an issue on GitHub.

Happy coding! 🚀
