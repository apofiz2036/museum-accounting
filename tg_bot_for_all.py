import os
from dotenv import load_dotenv
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'museum.settings')
django.setup()

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from bot_info.models import Subscribers, Categories

personal_data = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if Subscribers.objects.filter(tg_id=str(chat_id)).exists():
        context.bot.send_message(chat_id=chat_id, text='Вы уже зарегистрированы. Приятного использования!')
        return ConversationHandler.END
    else:
        keyboard = [[KeyboardButton('Начать работу')]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        text = (
            '🌟 Добро пожаловать в наш уютный уголок культуры! 🌟\n'
            'Здесь вы будете получать самые свежие новости и события из мира музея истории и этнографии. Давайте начнем!\n\n'
            'Если у вас возникнут вопросы или потребуется помощь, вы всегда можете написать нам: https://t.me/Apofiz2036 😊'
        )
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        return 'CHOOSING'


def agreement(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    keyboard = [[KeyboardButton('Согласен'), KeyboardButton('Не согласен')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    text = 'Для продолжения нам нужно ваше согласие на обработку персональных данных. Это важно для обеспечения вашего комфорта и безопасности.'
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    pdf_path = 'media/consents.pdf'
    with open(pdf_path, 'rb') as pdf_file:
        caption_text = 'Пожалуйста, уделите минутку, чтобы ознакомиться с этим документом. Ваше согласие поможет нам сделать ваше пребывание здесь ещё лучше!'
        context.bot.send_document(
            chat_id=chat_id,
            document=pdf_file,
            caption=caption_text
        )
    return 'CHOOSING'

def handle_agreement(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.text == 'Согласен':
        text = '🎉 Спасибо за ваше доверие! Теперь мы можем продолжить наше увлекательное путешествие по миру музея.'
        context.bot.send_message(chat_id=chat_id, text=text)
        return name_question(update, context)

    else:
        text = '😔 К сожалению, без вашего согласия мы не сможем продолжить. Пожалуйста, дайте нам шанс сделать ваше пребывание здесь ещё лучше!'
        context.bot.send_message(chat_id=chat_id, text=text)
        return agreement(update, context)

def name_question(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = '👤 Пожалуйста, представьтесь! Введите ваше ФИО, чтобы мы могли обращаться к вам по имени.'
    context.bot.send_message(chat_id=chat_id, text=text)
    return 'NAME_INPUT'

def name_input(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_name = update.message.text

    context.user_data['tg_id'] = str(chat_id)
    context.user_data['name'] = user_name
    context.user_data['phone'] = None
    context.user_data['categories'] = []

    text = '📱 Отлично! Теперь, пожалуйста, введите ваш номер телефона, чтобы мы могли оставаться на связи.'
    context.bot.send_message(chat_id=chat_id, text=text)
    return 'PHONE_INPUT'

def phone_input(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_phone = update.message.text
    context.user_data['phone'] = user_phone

    return categories(update, context)

def categories(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id  
    keyboard = [[KeyboardButton('Дошкольники'), KeyboardButton('Школьники')],
                [KeyboardButton('Студенты'), KeyboardButton('Взрослые')],
                [KeyboardButton('Мастера'), KeyboardButton('Активисты')],
                [KeyboardButton('Завершить выбор')]
                ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    text = '📚 Теперь давайте выберем категории, которые вам интересны! Вы можете выбрать несколько, чтобы получать только те новости, которые вас действительно увлекают.'
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    text = '🌟 Не стесняйтесь выбирать несколько категорий — чем больше, тем интереснее!'
    context.bot.send_message(chat_id=chat_id, text=text)
    return 'CHOOSING'

def handle_selection(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id 
    text = update.message.text

    if text == 'Завершить выбор':
        categories_list = context.user_data.get('categories', [])
        tg_id = context.user_data.get('tg_id')
        name = context.user_data.get('name')
        phone_number = context.user_data.get('phone')

        subscriber = Subscribers.objects.create(
            tg_id=tg_id,
            name=name,
            phone_number=phone_number
        )

        category_objects = Categories.objects.filter(category_name__in=categories_list)
        subscriber.categories.set(category_objects)

        subscriber.save()

        context.bot.send_message(chat_id=chat_id, text='🎉 Подписка успешно оформлена! Теперь вы будете в курсе всех самых интересных событий. Спасибо, что с нами!')
        return ConversationHandler.END
   
    else:
        if text not in context.user_data['categories']:
            context.user_data['categories'].append(text)
            context.bot.send_message(chat_id=chat_id, text='✅ Вы добавили: {}. Отличный выбор!'.format(text))
        else:
            context.bot.send_message(chat_id=chat_id, text='🤔 Эта категория уже выбрана: {}. Может, добавим ещё что-то интересное?'.format(text))
            
    return 'CHOOSING'

def main():
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN_FOR_ALL']
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'CHOOSING':[
                MessageHandler(Filters.regex('^Начать работу'), agreement),
                MessageHandler(Filters.regex('^Согласен'), handle_agreement),
                MessageHandler(Filters.regex('^Не согласен'), handle_agreement),
                MessageHandler(Filters.text, handle_selection)
            ],
            'NAME_INPUT':[
                MessageHandler(Filters.text & ~Filters.command, name_input)
            ],
            'PHONE_INPUT':[
                MessageHandler(Filters.text & ~Filters.command, phone_input)
            ]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()