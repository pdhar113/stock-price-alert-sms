import requests
from twilio.rest import Client
import os
import sys

print("[DEBUG] STOCK_API_KEY exists:", "STOCK_API_KEY" in os.environ)

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA Corporation"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ["STOCK_API_KEY"]

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params, timeout=30)
response.raise_for_status()
data = response.json()

print("API Response keys:", data.keys())

# ---- FIX: Handle rate limit / API errors safely ----
if "Time Series (Daily)" not in data:
    print("API Error Response:", data)
    sys.exit(0)

# ---- FIX: Do NOT rely on dict ordering ----
dates = sorted(data["Time Series (Daily)"].keys(), reverse=True)
yesterday_data = data["Time Series (Daily)"][dates[0]]
day_before_yesterday_data = data["Time Series (Daily)"][dates[1]]

yesterday_closing_price = float(yesterday_data["4. close"])
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

# ---- FIX: Add timeout ----
news_response = requests.get(NEWS_ENDPOINT, params=news_params, timeout=30)
news_response.raise_for_status()
news = news_response.json()

articles_with_description = [
    a for a in news.get("articles", []) if a.get("description")
]

three_articles = articles_with_description[:3]

# ---- Calculate percentage change ----
diff = yesterday_closing_price - day_before_yesterday_closing_price
diff_percent = (diff / day_before_yesterday_closing_price) * 100

up_down = "🔺" if diff_percent > 0 else "🔻"
print(f"Stock change: {up_down}{abs(diff_percent):.2f}%")

formatted_articles = [
    f"{STOCK_NAME}: {up_down}{abs(diff_percent):.2f}%\n"
    f"Headline: {article['title']}\n"
    f"Brief: {article['description']}"
    for article in three_articles
]

# ---- FIX: Meaningful alert condition ----
if abs(diff_percent) >= 5:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    twilio_from_number = os.environ["TWILIO_FROM_NUMBER"]
    twilio_to_number = os.environ["TWILIO_TO_NUMBER"]

    client = Client(account_sid, auth_token)

    # ---- FIX: Send ONE SMS instead of 3 ----
    message_body = "\n\n".join(formatted_articles)

    client.messages.create(
        body=message_body,
        from_=twilio_from_number,
        to=twilio_to_number,
    )