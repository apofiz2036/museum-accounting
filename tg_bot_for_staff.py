import os
from dotenv import load_dotenv
import django
from django.utils import timezone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'museum.settings')
django.setup()

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from events.models import EventsPlan
from time_off.models import TimeOff
from datetime import datetime


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    keyboard = [[KeyboardButton('Начать работу')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=chat_id, text='Добро пожаловать в бот для сотрудников музея истории и этнографии', reply_markup=reply_markup)


def main_menu(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    keyboard = [[KeyboardButton('Мероприятия на сегодня'), KeyboardButton('Запланированные мероприятия')],
                [KeyboardButton('Запланированные отгулы'), KeyboardButton('Свободные отгулы')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=chat_id, text='Выберете вариант запроса', reply_markup=reply_markup)

def begin_work(update: Update, context: CallbackContext):
    main_menu(update, context)

def event_today(update: Update, context: CallbackContext):
    tg_id = str(update.effective_chat.id)
    now = timezone.now()

    user_events = EventsPlan.objects.filter(employee__tg_id=tg_id, date=now.date())
    if user_events.exists():
        response = '\n'.join(
            [f"{event.event.event_name} - {event.date.strftime('%d.%m.%Y')} в {event.time.strftime('%H:%M')}. Комментарий: {event.comments}"
             for event in user_events]
        )  
    else:
        response = 'У вас нет запланированных мероприятий'

    update.message.reply_text(response)
    main_menu(update, context)


def events(update: Update, context: CallbackContext):
    tg_id = str(update.effective_chat.id)
    now = timezone.now()

    user_events = EventsPlan.objects.filter(employee__tg_id=tg_id, date__gte=now.date())
    if user_events.exists():
        response = '\n'.join(
            [f"{event.event.event_name} - {event.date.strftime('%d.%m.%Y')} в {event.time.strftime('%H:%M')}. Комментарий: {event.comments}"
             for event in user_events]
        )  
    else:
        response = 'У вас нет запланированных мероприятий'

    update.message.reply_text(response)
    main_menu(update, context)


def time_off(update: Update, context: CallbackContext):
    tg_id = str(update.effective_chat.id)
    now = timezone.now()

    user_time_off = TimeOff.objects.filter(employee__tg_id=tg_id, date_of_time_off__gte=now.date())
    if user_time_off.exists():
        response = '\n'.join(
            [f"Отгул: {day.date_of_time_off.strftime('%d.%m.%Y')} за ранее отработанное время: {day.date_work.strftime('%d.%m.%Y')}" for day in user_time_off]
        )
    else:
        response = 'У вас нет запланированных отгулов'

    update.message.reply_text(response)
    main_menu(update, context)


def free_time_off(update: Update, context: CallbackContext):
    tg_id = str(update.effective_chat.id)

    user_time_off = TimeOff.objects.filter(
        employee__tg_id=tg_id,
        date_of_time_off__isnull=True,
        double_payment=False
    )

    if user_time_off.exists():
        response = '\n'.join(
            [f"Свободный отгул за: {day.date_work.strftime('%d.%m.%Y')}" for day in user_time_off]
        )
    else:
        response = 'У вас нет свободных отгулов'
        
    update.message.reply_text(response)
    main_menu(update, context)


def main():
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN_EMPLOYEES']
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Начать работу$'), begin_work))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Мероприятия на сегодня$'), event_today))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Запланированные мероприятия$'), events))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Запланированные отгулы$'), time_off))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Свободные отгулы$'), free_time_off))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()