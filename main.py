from dotenv import load_dotenv
import logging
import os
import requests

from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from handlers.rssparse import ctf_time_update
from handlers.finance import get_ticker_history

logging.basicConfig(
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv("TOKEN")
url = "https://api.telegram.org/bot" + token + "/getMe"
r = requests.get(url)
d = r.json()
name = d["result"]["first_name"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(user)
    await update.message.reply_html(
        rf"Hello {user.mention_html()}! I am " + name + "!",
        reply_markup=ForceReply(selective=True),
        )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Command list:\n"
                                    f"/ctf - list CTFs happening this week\n"
                                    f"/chart <ticker> - chart financial history graph of given ticker"
                                    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ctf", ctf_time_update))
    application.add_handler((CommandHandler("chart", get_ticker_history)))
    application.add_handler(CommandHandler("help", help))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
