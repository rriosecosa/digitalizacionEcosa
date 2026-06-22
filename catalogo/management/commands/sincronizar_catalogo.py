from django.core.management.base import BaseCommand

from catalogo.models import (
    Producto,
    ProductoCatalogo
)


class Command(BaseCommand):

    help = "Sincroniza productos WMS con catálogo"

    def handle(self, *args, **kwargs):

        creados = 0

        productos = Producto.objects.filter(
            habilitado=1,
            eliminado=0
        )

        for producto in productos:

            _, created = (
                ProductoCatalogo.objects.get_or_create(
                    producto=producto
                )
            )

            if created:
                creados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Se crearon {creados} registros'
            )
        )