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

        info = ticker.info
        name = info.get("longName", "Data not available")
        exchange = info.get("exchange", "Data not available")
        currency = info.get("currency", "Data not available")

        currentPrice = info.get("currentPrice", "Data not available")
        netIncomeToCommon = info.get("netIncomeToCommon", "Data not available")
        trailingEps = info.get("trailingEps", "Data not available")
        returnOnEquity = info.get("returnOnEquity", "Data not available")
        profitMargins = info.get("profitMargins", "Data not available")
        revenueGrowth = info.get("revenueGrowth", "Data not available")
        earningsGrowth = info.get("earningsGrowth", "Data not available")
        debtToEquity = info.get("debtToEquity", "Data not available")
        currentRatio = info.get("currentRatio", "Data not available")
        dividendYield = info.get("dividendYield", "Data not available")
        payoutRatio = info.get("payoutRatio", "Data not available")
        priceToBook = info.get("priceToBook", "Data not available")
        freeCashFlow = info.get("freeCashflow", "Data not available")

        if type(currentPrice) == str or type(trailingEps) == str:
            priceToEarnings = "Data not available"
        else:
            priceToEarnings = currentPrice / trailingEps

        await update.message.reply_text(f"""
            Current Price: {currentPrice} {currency} 
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
            \nDividend Health:
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
