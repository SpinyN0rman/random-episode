from django.apps import AppConfig


class RandomEpisodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'random_episode'

    def ready(self):
        import random_episode.signals  # noqa: F401
