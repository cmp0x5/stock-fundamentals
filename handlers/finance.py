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

        currentPrice = ticker.info["currentPrice"]
        netIncomeToCommon = ticker.info["netIncomeToCommon"]
        trainingEps = ticker.info["trailingEps"]
        returnOnEquity = ticker.info["returnOnEquity"] * 100
        profitMargins = ticker.info["profitMargins"] * 100
        revenueGrowth = ticker.info["revenueGrowth"] * 100
        earningsGrowth = ticker.info["earningsGrowth"] * 100
        debtToEquity = ticker.info["debtToEquity"]
        currentRatio = ticker.info["currentRatio"]
        dividendYield = ticker.info["dividentYield"] * 100
        payoutRatio = ticker.info["payoutRatio"] * 100
        priceToEarnings = currentPrice / trailingEps
        priceToBook = ticker.info["priceToBook"]
        freeCashFlow = ticker.info["freeCashflow"]

        await update.message.reply_text(f"""
            Current Price: {currentPrice} {currency} 
            \nResults for fiscal year {ticker.info["fiscalYear"]}:
            \nProfitability:
            \nNet Income To Common Shareholders: {netIncomeToCommon} {currency} 
            \nEarnings Per Share: {trailingEps} {currency} 
            \nReturn on Equity: {returnOnEquity}%
            \nProfit Margin: {profitMargins}%
            \nGrowth Indicators:
            \nRevenue Growth: {revenueGrowth}%
            \nEarnings Growth: {earningsGrowth}%
            \nFinancial Health:
            \nDebt to Equity: {debtToEquity}%
            \nCurrent Ratio: {currentRatio} 
            \nDivident Health:
            \nDividend Yield: {dividendYield}%
            \nPayout Ratio: {payoutRatio}%
            \nValuation Metrics:
            \nP/E: {priceToEarnings}
            \nP/B: {priceToBook}
            \nCash Flow:
            \nFree Cash Flow: {freeCashFlow} {currency} 
        """)

        var = (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100
        if (var > 0):
            sign = "+"
            line_color = "green"
        else:
            sign = ""
            line_color = "red"

        plt.figure(figsize=(10,6))
        plt.plot(data.index, data["Close"], label=f"{name}", color=line_color)
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
