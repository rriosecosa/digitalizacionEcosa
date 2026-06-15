from django.views.generic import TemplateView

from catalogo.models import (
    Proveedor,
    Familia,
    Producto
)


class HomeView(TemplateView):

    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['marcas'] = (
            Proveedor.objects
            .exclude(marca__isnull=True)
            .exclude(marca='')
            .order_by('marca')[:12]
        )

        context['categorias'] = (
            Familia.objects
            .exclude(titulo__isnull=True)
            .exclude(titulo='')
            .order_by('titulo')[:8]
        )

        context['total_productos'] = (
            Producto.objects.filter(
                habilitado=1,
                eliminado=0
            ).count()
        )

        return context