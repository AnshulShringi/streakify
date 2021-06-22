from django.apps import AppConfig


class StreakAppConfig(AppConfig):
    name = 'streakify.streak_app'

    def ready(self):
        import streakify.streak_app.signals
