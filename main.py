import logging
import telegram 
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import time
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

api = "1468499223:AAF1-zRu-S_xp1zT0vWwmGHQ6KyemKMf_wk"
bot = telegram.Bot(token = api)

def main() : 
    updater = Updater("1468499223:AAF1-zRu-S_xp1zT0vWwmGHQ6KyemKMf_wk", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_message))
    dispatcher.add_handler(CommandHandler('upload', upload)) 
    updater.start_polling()
    updater.idle()  

def get_message(update : telegram.Update, context: CallbackContext) :
        global Text 
        Text = update.message.text
        update.message.reply_text(
            "이 메세지를 업로드하실겁니까? 만약 그렇다면 /upload 라고 입력해주세요.\n"
            "전달할 메세지 :\n"+Text
        )

def upload(update : telegram.Update, context : CallbackContext) :
    if Text != None :
        bot.send_message(chat_id = '@koreanagora', text= "#AGORA\n\n" + Text)

if __name__ == '__main__':
    main()
