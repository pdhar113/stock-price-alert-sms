import requests
from twilio.rest import Client
import os

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA Corporation"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ["STOCK_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
TWILIO_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
VIRTUAL_TWILIO_NUMBER = os.environ["TWILIO_FROM_NUMBER"]
VERIFIED_NUMBER = os.environ["TWILIO_TO_NUMBER"]

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

yresponse = requests.get(STOCK_ENDPOINT, params=stock_params)
ydata = yresponse.json()
if "Time Series (Daily)" not in ydata:
    print("[ERROR] API response does not contain 'Time Series (Daily)':", ydata)
    raise SystemExit("Failed to get stock data. Check API response above.")
data = ydata["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# Find the positive difference between 1 and 2
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

# STEP 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles
    three_articles = articles[:3]

    # Create a new list of the first 3 article's headline and description using list comprehension
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles
    ]

    # Send each article as a separate message via Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article, from_=VIRTUAL_TWILIO_NUMBER, to=VERIFIED_NUMBER
        )
