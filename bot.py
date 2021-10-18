

# Bitly Bot

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from os import environ
from pyrogram import Client, filters
from pyshorteners import Shortener


API_ID = int(environ.get('API_ID'))
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
BITLY_KEY = environ.get('BITLY_KEY')
OWNER = environ.get('OWNER','Kamdev07')

SHORTLINKBOT = Client('ShortlinkBot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)
             
             

@SHORTLINKBOT.on_message(filters.command(['start','help']))
async def start(_, update):
    
    await update.reply(
        f"**Hi {update.chat.first_name}!**\n\n"
        "I'm shortlink bot. Just send me link and get adsless short link",
        )

@SHORTLINKBOT.on_message(filters.regex(r'https?://[^\s]+'))
async def link_handler(_, update):
    link = update.matches[0].group(0)
    shortened_url, Err = get_shortlink(link)
    if shortened_url is None:
        message = f"Something went wrong \n{Err}"
        await update.reply(message, quote=True)
        return
    message = f"Here is your shortlink\n {shortened_url}"
    # i don't think this bot with get sending message error so no need of exceptions
    await update.reply_text(text=message, reply_markup=markup, quote=True)
      
def get_shortlink(url):
    shortened_url = None
    Err = None
    try:
        ''' Bittly Shorten'''
        s = Shortener(api_key=BITLY_KEY)
        shortened_url = s.bitly.short(url)
     
    except Exception as error:
        Err = f"#ERROR: {error}"
        log.info(Err)
    return shortened_url,Err
        
        
if __name__ == "__main__" :
    log.info(">>Bot-Started<<")
    SHORTLINKBOT.run()
