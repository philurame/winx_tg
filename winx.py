import random
import time
import numpy as np

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater, MessageHandler, Filters

import gensim.downloader

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


TOKEN = '5504954650:AAG604-ipWZYHILipgwrKB8jLxPXFgTLKMw'

#MEMORY={id:{q1:a1,q2:a2,...},...}
MEMORY = {}

buttons = [InlineKeyboardButton(text='A', callback_data=f'A'),InlineKeyboardButton(text='B',callback_data='B'),\
            InlineKeyboardButton(text='C', callback_data=f'C'),InlineKeyboardButton(text='D', callback_data='D')]

questions = {
    'твоё любимое место в Алфее:\nA) уголок интроверта\nB) фреш бар\nC) vk fest\nD) рок-комната на 2 этаже':[1,4,5,5],
    'моя сильная сторона:\nA) SRE\nB) WEB \nC) ML \nD) волшебная пыль':[1,1,1,2],
    'какую суперсилу ты хотела бы получить:\nA) силу солнца!\nB) java\nC) haskell\nD) с++':[2,1,7,1],
    'любимый вкус:\nA) маржинальная вишня\nB) мотивированный лимон \nC) конверсионный апельсин\nD) поражения':[3,0,2,6],
    'после ты предпочла бы:\nA) поспать в \nB) поспать  \nC) ML \nD) волшебную пыль':[7,7,1,2],
    'чего ты боишься больше всего:\nA) не успеть и опоздать\nB) монстров\nC) поражения\nD) победы':[3,2,0,6],
    'какого ты роста?\nA) линейный \nB) экспоненциальный \nC) логарифмический \nD) константный':[2,0,4,5],
    'что ты предпочитаешь из еды?\nA) кофе с печенкой \nB) фруктик  \nC) пиво \nD) доставка':[1,4,0,6],
    'со сколькими феечками ты успел познакомиться?\nA) со всеми феечками \nB) три феечки  \nC) две феечки \nD) нет':[2,0,4,1],
    'сколько тебе лет на вид?\nA) 15 (но я матерюсь)\nB) ноль  \nC) нормально \nD) я считаю это не этично спрашивать у юной феи ее возраст (я старая)':[2,0,5,7],
    'расскажи немного о себе:\nA) я люблю бравл старс, у меня есть много скинов\nB) не скажу\nC) я милая) люблю пчел\nD) не скажу 2':[8,1,4,5],
    'вареники, пельмени, пельменики или варени?':[3,3,3,3],
    'ты с подружками отправилась в кафе, какой сок ты выберешь?\nA) апельсиновый\nB) морковный\nC) грейпфрутовый\nD) яблочный':[2,7,3,4],
    'какого ты хочешь парня?\nA) скай\nB) красивого \nC) валтор \nD) я еще думаю':[0,2,6,7],
    'кто ты из лиги легенд?\nA) люкс\nB) сона\nC) серафина\nD) ясуо':[0,4,5,8],
}
blockPrint()
vectors = gensim.downloader.load('word2vec-ruscorpora-300')
enablePrint()

def word2key(word, vectors):
    if word+'_NOUN' in vectors:
        return word+'_NOUN'
    elif word+'_ADJ' in vectors:
        return word+'_ADJ'
    elif word+'_VERB' in vectors:
        return word+'_VERB'
    elif word+'_NUM' in vectors:
        return word+'_VERB'
    elif word+'_DET' in vectors:
        return word+'_DET'
    elif word+'_DET' in vectors:
        return word+'_DET'
    elif word+'_NUM' in vectors:
        return word+'_NUM'
    elif word+'_PRON' in vectors:
        return word+'_PRON'
    elif word+'_PART' in vectors:
        return word+'_PART'
    elif word+'_ADP' in vectors:
        return word+'_ADP'
    elif word+'_CCONJ' in vectors:
        return word+'_CCONJ'
    elif word+'_INTJ' in vectors:
        return word+'_INTJ'
    return None

def execute(expression,vectors):
    res=[np.array([0]*300)]
    plus=list(map(lambda x: x.strip(),expression.split('+')))
    negative=False
    if plus[0][0]=='-':
        negative=True
    indic=1
    for i in plus:
        if indic and negative:
            minus=list(map(lambda x: x.strip(),i.split('-')))[1:]
        else:
            minus=list(map(lambda x: x.strip(),i.split('-')))
        word=word2key(minus[0],vectors)
        if not word:
            return None
        if indic and negative:
            res-=vectors[word]
        else:
            res+=vectors[word]
        for j in minus[1:]:
            word=word2key(j,vectors)
            if not word:
                return None
            res-=vectors[word]
    res=vectors.similar_by_vector(res[0])[:3]
    return [res[0][0].split('_')[0],res[1][0].split('_')[0],res[2][0].split('_')[0]]





def generate_question(passed_questions) -> str:
    residual=list(set(questions) - set(passed_questions))
    if not residual:
        return None
    num = random.randrange(len(residual))
    return residual[num]

def already_fairy(update):
    list_to_fairy={0:'БЛУМ',1:'ТЕКНА',2:'СТЕЛЛА',3:'ЛЕЙЛА',4:'ФЛОРА',5:'МУЗА',6:'АЙСИ',7:'ФАРАГОНДА',8:'ЯСУО'}
    fairy={'БЛУМ':0,'ТЕКНА':0,'СТЕЛЛА':0,'ЛЕЙЛА':0,'ФЛОРА':0,'МУЗА':0,'АЙСИ':0,'ФАРАГОНДА':0,'ЯСУО':0}

    chat_id=update.callback_query.message.chat_id
    for question in MEMORY[chat_id]:
        if MEMORY[chat_id][question] not in [i for i in range(9)]:
            continue
        fairy[list_to_fairy[questions[question][MEMORY[chat_id][question]]]]+=1
        if questions[question][MEMORY[chat_id][question]]==8:
            MEMORY.pop(chat_id)
            update.callback_query.message.reply_text("О НЕТ! ВИНКС НЕ СМОГУТ ВЗЯТЬ ТЕБЯ В СВОЮ КОМАНДУ!\n ВОЗЬМИ /enchantix И ПОПРОБУЙ ЕЩЕ РАЗ СТАТЬ /winx!")
            return True
    winner=max(fairy, key=fairy.get)
    if (len(MEMORY[chat_id])==len(questions)) or (fairy[winner]>=2):
        MEMORY.pop(chat_id)
        update.callback_query.message.reply_text(f"УРА!! ТЫ {winner}")
        update.callback_query.message.reply_text(f'{winner}! не забудь использовать волшебную пыль /enchantix!')
        return True

    return False

def start_command(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text('привет, прекрасная фея!\nузнай кто ты из /winx или возьми усиление /enchantix!')
        chat_id = update.message.chat_id
        MEMORY[chat_id]={}
    except:
        MEMORY.pop(chat_id)
def winx_command(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text('если решишь')
        time.sleep(0.5)
        update.message.reply_text('можешь ты стать')
        time.sleep(0.6)
        update.message.reply_text('одной из нас!')
        time.sleep(1)
        chat_id = update.message.chat_id
        MEMORY[chat_id]={}
        question=generate_question([])
        MEMORY[chat_id][question]=None
        update.message.reply_text(
            question, reply_markup=InlineKeyboardMarkup([buttons]),
        )
    except:
        MEMORY.pop(chat_id)
def enchantix_command(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text('О-О-О!')
        time.sleep(1)
        update.message.reply_text('энчантиикс!')
        time.sleep(1)
        update.message.reply_text('волшебная пыыль!')
        time.sleep(1)
        update.message.reply_text('максимум сиилы!')
    except:
        chat_id = update.message.chat_id
        MEMORY.pop(chat_id)
def A_query(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = update.callback_query.message.chat_id
        prev_question = update.callback_query.message.text
        MEMORY[chat_id][prev_question]=0

        question = generate_question(list(MEMORY[chat_id].keys()))
        MEMORY[chat_id][question]=None
        if already_fairy(update):
                return
        update.callback_query.message.reply_text(
            question, reply_markup=InlineKeyboardMarkup([buttons]),
        )
    except:
        chat_id = update.message.chat_id
        MEMORY.pop(chat_id)
def B_query(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = update.callback_query.message.chat_id
        prev_question = update.callback_query.message.text
        MEMORY[chat_id][prev_question]=1

        question = generate_question(list(MEMORY[chat_id].keys()))
        MEMORY[chat_id][question]=None
        if already_fairy(update):
            return
        update.callback_query.message.reply_text(
            question, reply_markup=InlineKeyboardMarkup([buttons]),
        )
    except:
        chat_id = update.message.chat_id
        MEMORY.pop(chat_id)
def C_query(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = update.callback_query.message.chat_id
        prev_question = update.callback_query.message.text
        MEMORY[chat_id][prev_question]=2

        question = generate_question(list(MEMORY[chat_id].keys()))
        MEMORY[chat_id][question]=None
        if already_fairy(update):
            return
        update.callback_query.message.reply_text(
            question, reply_markup=InlineKeyboardMarkup([buttons]),
        )
    except:
        chat_id = update.message.chat_id
        MEMORY.pop(chat_id)
def D_query(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = update.callback_query.message.chat_id
        prev_question = update.callback_query.message.text
        MEMORY[chat_id][prev_question]=3

        question = generate_question(list(MEMORY[chat_id].keys()))
        MEMORY[chat_id][question]=None
        if already_fairy(update):
            return
        update.callback_query.message.reply_text(
            question, reply_markup=InlineKeyboardMarkup([buttons]),
        )
    except:
        chat_id = update.message.chat_id
        MEMORY.pop(chat_id)

def _clear_command(update: Update, context: CallbackContext) -> None:
    global MEMORY
    MEMORY={}
    update.message.reply_text('Валтор стёр всю материю с лица Алфеи...')

def handle_everything_else(update: Update, context: CallbackContext):
    text=update.message.text.lower()
    if '+' in text or '-' in text:
        res=execute(text,vectors)
        if not res:
            update.message.reply_text('не пониматб')
            return
        update.message.reply_text('бум! получилось что то типа ' + ', или '.join(res)+'...')
        return
    update.message.reply_text('не пониматб')
handlers = [
    CommandHandler('start', start_command),
    CommandHandler('enchantix', enchantix_command),
    CommandHandler('winx', winx_command),
    CommandHandler('_clear', _clear_command),

    CallbackQueryHandler(A_query, pattern='A'),
    CallbackQueryHandler(B_query, pattern='B'),
    CallbackQueryHandler(C_query, pattern='C'),
    CallbackQueryHandler(D_query, pattern='D'),
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