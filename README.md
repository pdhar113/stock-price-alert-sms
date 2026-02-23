# Stock News SMS Alert

This project checks the daily price change for a stock (e.g., NVDA) and sends you news headlines via SMS if the change exceeds a threshold.

## Features
- Fetches daily stock data from Alpha Vantage
- Gets latest news headlines from NewsAPI
- Sends SMS alerts using Twilio
- Automated with GitHub Actions (scheduled or manual)
- All secrets managed securely via GitHub Actions secrets

## Setup
1. **Clone the repo**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables** (for local testing):
   - STOCK_API_KEY
   - NEWS_API_KEY
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - TWILIO_FROM_NUMBER
   - TWILIO_TO_NUMBER

   Example (PowerShell):
   ```powershell
   $env:STOCK_API_KEY="your_key"
   # ...set others similarly
   ```

4. **Run the script**
   ```bash
   python main.py
   ```

## GitHub Actions Automation
- Add all secrets in your repo's Settings > Secrets and variables > Actions
- Workflow runs daily at 6:00 AM IST (00:30 UTC) and can be triggered manually

## Customization
- Change `STOCK_NAME` and `COMPANY_NAME` in `main.py` to monitor a different stock
- Adjust the threshold in `main.py` (default: 5%)


