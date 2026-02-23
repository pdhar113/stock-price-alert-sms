
# Stock Price Alert SMS

A Python automation project that monitors daily stock price changes and sends you news headlines via SMS if the change exceeds a threshold. Runs automatically on a schedule using GitHub Actions.

## Features
- Fetches daily stock data from Alpha Vantage
- Gets latest news headlines from NewsAPI
- Sends SMS alerts using Twilio
- Fully automated with GitHub Actions (scheduled and manual runs)
- All secrets managed securely via GitHub Actions secrets

## How It Works
1. The script checks the daily closing price for a stock (default: NVDA)
2. If the price change (up or down) is greater than a threshold (default: 5%), it fetches the latest news headlines
3. Sends you an SMS with the stock change and news headlines
4. If the Alpha Vantage API rate limit is reached, you get an SMS notification

## Quick Start

### 1. Clone the Repo
```bash
git clone https://github.com/pdhar113/stock-price-alert-sms.git
cd stock-price-alert-sms
```

### 2. Install Dependencies (for local testing)
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables (for local testing)
Set these in your terminal or system environment:
- `STOCK_API_KEY` (Alpha Vantage)
- `NEWS_API_KEY` (NewsAPI.org)
- `TWILIO_ACCOUNT_SID` (Twilio)
- `TWILIO_AUTH_TOKEN` (Twilio)
- `TWILIO_FROM_NUMBER` (Twilio phone number)
- `TWILIO_TO_NUMBER` (Your phone number)

Example (PowerShell):
```powershell
$env:STOCK_API_KEY="your_key"
$env:NEWS_API_KEY="your_key"
$env:TWILIO_ACCOUNT_SID="your_sid"
$env:TWILIO_AUTH_TOKEN="your_token"
$env:TWILIO_FROM_NUMBER="+1234567890"
$env:TWILIO_TO_NUMBER="+919999999999"
```

### 4. Run the Script Locally
```bash
python main.py
```

## GitHub Actions Automation
- Add all secrets in your repo's **Settings > Secrets and variables > Actions**
- The workflow runs daily at **6:00 AM IST (00:30 UTC)** and can also be triggered manually from the Actions tab

## Customization
- Change `STOCK_NAME` and `COMPANY_NAME` in `main.py` to monitor a different stock
- Adjust the threshold in `main.py` (default: 5%)
- Edit the workflow schedule in `.github/workflows/python-app.yml` as needed

## Troubleshooting
- **No SMS received?**
  - Check the Actions run logs for errors or debug output
  - Make sure your Twilio account is set up and your recipient number is verified (if using a trial account)
  - Lower the threshold in `main.py` to force an SMS for testing
- **API rate limit reached?**
  - You will receive an SMS notification when this happens

## License
MIT


