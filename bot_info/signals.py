from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Message, Subscribers
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN_FOR_ALL']

bot = Bot(token=TELEGRAM_TOKEN)

@receiver(m2m_changed, sender=Message.categories.through)
def send_message(sender, instance, action, **kwargs):
    if action == "post_add":
        text = instance.text_message
        categories = instance.categories.all()

        tg_ids = []

        for category in categories:
            subscribers = Subscribers.objects.filter(categories=category)
            for subscriber in subscribers:
                tg_ids.append(subscriber.tg_id)

        tg_ids = list(set(tg_ids))

        for tg_id in tg_ids:
            if tg_id:
                if instance.image:
                    with open(instance.image.path, 'rb') as photo:
                        bot.send_photo(chat_id=tg_id, photo=photo, caption=text)
                else:
                    bot.send_message(chat_id=tg_id, text=text)
