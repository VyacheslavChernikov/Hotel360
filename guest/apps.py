from django.apps import AppConfig

class GuestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guest'  # Это имя приложения (должно совпадать с названием папки)
    verbose_name = 'Гости'  # Это отображаемое название в админке