from django.apps import AppConfig

class BotappConfig(AppConfig):
    name = 'botapp'

    def ready(self):
        from .views import set_webhook
        set_webhook()
