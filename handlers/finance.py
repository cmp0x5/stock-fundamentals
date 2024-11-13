from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf

async def get_ticker_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        stock = update.message.text[7:]
        await update.message.reply_text(f"Searching for ticker \"{stock}\"...")
        if len(stock) > 10:
            await update.message.reply_text(f"Invalid ticker!")
            return
        
        ticker = yf.Ticker(stock)
        data = ticker.history(period="max")
        if data.empty:
            await update.message.reply_text(f"Ticker not found!")
            return

        name = ticker.info["longName"]
        exchange = ticker.info["exchange"]
        currency = ticker.info["currency"]

        var = (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100
        sign = "+" if var > 0 else ""

        plt.figure(figsize=(10,6))
        plt.plot(data.index, data["Close"], label=f"{name}")
        plt.xlabel("Date")
        plt.ylabel(f"Closing Price")
        plt.title(f"{name} ({currency})\n"
                f"{sign}"
                f"{var:.2f}% over period",
                fontsize=14,
                color="black",
                )

        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        #plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        #plt.gcf().autofmt_xdate()

        plt.legend()
        plt.grid(True)
        plt.savefig(f"chart.jpg")
        plt.close()
        with open(f"chart.jpg", "rb") as chart:
            await update.message.reply_photo(photo=chart, caption=f"{name} values over time")
    except Exception as e:
        print(f"Error: {e}")
