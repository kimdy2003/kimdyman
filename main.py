import logging
import telegram 
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import time
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telegram.Bot(token = '1661961084:AAEsBr-JTf5UkeCmaJNjrM5Tk8aeEet6ebM')

def main() : 
    updater = Updater("1661961084:AAEsBr-JTf5UkeCmaJNjrM5Tk8aeEet6ebM", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_message))
    updater.start_polling()
    updater.idle()  

def get_message(update : telegram.Update, context: CallbackContext) :
    if update.message.text != None :
        bot.send_message(chat_id = -1001424041679, text= update.message.text)
        update.message.reply_text("성공적으로 전송되었습니다.")
        user = update.message.from_user
        try :
            fname = user.first_name
        except :
            fname = ""
        try : 
            lname = user.last_name
        except :
            lname = ""
        try :
            username = user.username
        except :
            username = ""
        userid = user.id
        contents = str(lname)+" "+str(fname)+"  @"+str(username)+" id:"+str(userid)+"\n\n"+update.message.text
        bot.send_message(chat_id = -1001251638746, text= contents)

if __name__ == '__main__':
    main()
