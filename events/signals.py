from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import EventsPlan, Staff
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN_EMPLOYEES']

bot = Bot(token=TELEGRAM_TOKEN)

@receiver(m2m_changed, sender=EventsPlan.employee.through)
def send_event_notification(sender, instance, action, **kwargs):
    if action == "post_add":
        message = f'У вас запланировано новое мероприятие {instance.event.event_name} на {instance.date.strftime("%d.%m.%Y")} в {instance.time.strftime("%H:%M")}. Комментарий: {instance.comments}.'
        employees = instance.employee.all()

        if employees:
            for employe in employees:
                tg_id = employe.tg_id
                if tg_id:
                    bot.send_message(chat_id=tg_id, text = message)
