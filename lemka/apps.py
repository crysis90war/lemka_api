from django.apps import AppConfig


class LemkaConfig(AppConfig):
    name = 'lemka'

    def ready(self):
        import lemka.signals
