from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # docs recommend it that way
    def ready(self):
        # import signals(creating profile for each registered user)
        import users.signals
