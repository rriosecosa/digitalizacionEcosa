from django.apps import AppConfi

class BodegaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bodega'

    def ready(self):
        import bodega.signals # Carga la lógica de separación automatizada



        