from django.apps import AppConfig


class BotInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_info'
    verbose_name = 'Информационный бот'

    def ready(self):
        import bot_info.signals
