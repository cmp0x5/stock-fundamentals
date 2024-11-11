from telegram import Update
from telegram.ext import ContextTypes
import asyncio
import feedparser
from datetime import datetime, timezone, timedelta

def get_feed(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    #print(entries[0].keys())
    return entries

async def ctf_time_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("CTF notifications turned on")
    while True:
        now_timestamp = int(datetime.now(timezone.utc).timestamp())
        entries = get_feed("https://ctftime.org/event/list/upcoming/rss")
        for a in entries:
            start_time = a.start_date
            start_time = datetime.strptime(start_time, "%Y%m%dT%H%M%S") # apparently utc-1
            event_timezone = timezone(timedelta(hours=-1))
            start_time = start_time.replace(tzinfo=event_timezone)
            start_time_utc = start_time.astimezone(timezone.utc)
            start_timestamp = int(start_time_utc.timestamp())
            days_until = (start_timestamp - now_timestamp) / 86400
            display_time = start_time_utc.strftime('%b %d, %Y %H:%M')
            if days_until < 2:
                await update.message.reply_text(f'CTF starting soon:\n{a.title}\n{display_time}\n{a.link}')
        await asyncio.sleep(60)

