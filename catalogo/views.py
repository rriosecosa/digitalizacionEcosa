from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import (
    Producto,
    Familia,
    Proveedor
)


class CatalogoView(ListView):

    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 24

    def get_queryset(self):

        queryset = (
            Producto.objects
            .filter(
                habilitado=1,
                eliminado=0
            )
            .select_related(
                'familia',
                'proveedor',
                'medida'
            )
        )

        q = self.request.GET.get('q', '').strip()
        categoria = self.request.GET.get('categoria')
        marca = self.request.GET.get('marca')

        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) |
                Q(codigo__icontains=q) |
                Q(proveedor__marca__icontains=q)
            )

        if categoria:
            queryset = queryset.filter(
                familia_id=categoria
            )

        if marca:
            queryset = queryset.filter(
                proveedor_id=marca
            )

        return queryset.order_by('titulo')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['categorias'] = (
            Familia.objects
            .exclude(titulo__isnull=True)
            .exclude(titulo='')
            .order_by('titulo')
        )

        context['marcas'] = (
            Proveedor.objects
            .exclude(marca__isnull=True)
            .exclude(marca='')
            .order_by('marca')
        )

        context['total_productos'] = (
            Producto.objects.filter(
                habilitado=1,
                eliminado=0
            ).count()
        )

        return context


class ProductoDetalleView(DetailView):

    model = Producto

    template_name = 'catalogo/detalle_producto.html'

    context_object_name = 'producto'

    pk_url_kwarg = 'id'

    queryset = (
        Producto.objects
        .filter(
            habilitado=1,
            eliminado=0
        )
        .select_related(
            'familia',
            'proveedor',
            'medida'
        )
    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['productos_relacionados'] = (
            Producto.objects
            .filter(
                familia=self.object.familia,
                habilitado=1,
                eliminado=0
            )
            .exclude(
                id=self.object.id
            )
            .select_related(
                'familia',
                'proveedor'
            )[:4]
        )

        return context