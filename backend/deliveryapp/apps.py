from django.apps import AppConfig

class DeliveryappConfig(AppConfig):
    name = 'deliveryapp'

    def ready(self):
        # import signals so they're registered
        import deliveryapp.signals  # noqa
