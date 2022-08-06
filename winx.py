from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater, MessageHandler, Filters

TOKEN = '5402875904:AAFkX76VxCNv1oUicVRguyOGQ6n-CRZHU1M'

def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('привет, прекрасная фея!\nузнай кто ты из /winx или возьми усиление /enchantix!\nеще ты можешь использовать магию слов!')

def handle_everything_else(update: Update, context: CallbackContext):
    update.message.reply_text('сам ты '+update.message.text)


handlers = [
    CommandHandler('start', start_command),
    MessageHandler(Filters.all, handle_everything_else)
]

def main() -> None:
    updater = Updater(TOKEN, workers=100)
    for handler in handlers:
        updater.dispatcher.add_handler(handler)
    updater.start_polling()
    print('Start bot')
    updater.idle()

if __name__ == '__main__':
    main()
