# from django.apps import AppConfig


# class UserappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'userapp'



from django.apps import AppConfig

class UserappConfig(AppConfig):
    name = 'userapp'

    def ready(self):
        # import signals to ensure registration
        import userapp.signals  # noqa
