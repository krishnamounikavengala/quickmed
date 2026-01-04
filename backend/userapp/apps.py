


from django.apps import AppConfig

class UserappConfig(AppConfig):
    name = 'userapp'

    def ready(self):
        # import signals to ensure registration
        import userapp.signals  # noqa
