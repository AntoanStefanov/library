from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # docs recommend it that way
    def ready(self):
        # register signals
        import users.signals
