from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto, Familia, Proveedor


class CatalogoView(ListView):

    model = Producto
    template_name = "catalogo/catalogo.html"
    context_object_name = "productos"
    paginate_by = 24

    def get_queryset(self):

        queryset = Producto.objects.filter(habilitado=1, eliminado=0).select_related(
            "familia", "proveedor", "medida"
        )

        q = self.request.GET.get("q", "").strip()
        categoria = self.request.GET.get("categoria")
        marca = self.request.GET.get("marca")

        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q)
                | Q(codigo__icontains=q)
                | Q(proveedor__marca__icontains=q)
            )

        if categoria:
            queryset = queryset.filter(familia_id=categoria)

        if marca:
            queryset = queryset.filter(proveedor_id=marca)

        return queryset.order_by("titulo")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categorias"] = (
            Familia.objects.exclude(titulo__isnull=True)
            .exclude(titulo="")
            .order_by("titulo")
        )

        context["marcas"] = (
            Proveedor.objects.exclude(marca__isnull=True)
            .exclude(marca="")
            .order_by("marca")
        )

        context["total_productos"] = Producto.objects.filter(
            habilitado=1, eliminado=0
        ).count()

        return context


class ProductoDetalleView(DetailView):

    model = Producto

    template_name = "catalogo/detalle_producto.html"

    context_object_name = "producto"

    pk_url_kwarg = "id"

    queryset = Producto.objects.filter(habilitado=1, eliminado=0).select_related(
        "familia", "proveedor", "medida"
    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["productos_relacionados"] = (
            Producto.objects.filter(
                familia=self.object.familia, habilitado=1, eliminado=0
            )
            .exclude(id=self.object.id)
            .select_related("familia", "proveedor")[:4]
        )

        return context


from django.contrib.auth.models import Group

def login_catalogo(request):

    if request.user.is_authenticated:
        return redirect('dashboard_catalogo')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            if (
                user.is_superuser
                or
                user.groups.filter(
                    name='CATALOGO_ADMIN'
                ).exists()
            ):

                login(
                    request,
                    user
                )

                return redirect(
                    'dashboard_catalogo'
                )

            messages.error(
                request,
                'No tienes permisos para acceder.'
            )

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos'
            )

    return render(
        request,
        'catalogo/admin/login.html'
    )


def logout_catalogo(request):

    logout(request)

    return redirect("login_catalogo")


from catalogo.models import Producto, Familia, Proveedor, ProductoCatalogo

from .decorators import catalogo_required

@login_required
@catalogo_required
def dashboard_catalogo(request):

    total_productos = Producto.objects.filter(habilitado=1, eliminado=0).count()

    total_categorias = Familia.objects.count()

    total_marcas = Proveedor.objects.count()

    con_imagen = (
        Producto.objects.filter(habilitado=1, eliminado=0)
        .exclude(imagen__isnull=True)
        .exclude(imagen="")
        .count()
    )

    sin_imagen = total_productos - con_imagen

    con_descripcion = (
        ProductoCatalogo.objects.exclude(descripcion_catalogo__isnull=True)
        .exclude(descripcion_catalogo="")
        .count()
    )

    sin_descripcion = total_productos - con_descripcion

    porcentaje_imagenes = (
        round((con_imagen / total_productos) * 100, 1) if total_productos else 0
    )

    porcentaje_descripciones = (
        round((con_descripcion / total_productos) * 100, 1) if total_productos else 0
    )

    context = {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_marcas": total_marcas,
        "con_imagen": con_imagen,
        "sin_imagen": sin_imagen,
        "con_descripcion": con_descripcion,
        "sin_descripcion": sin_descripcion,
        "porcentaje_imagenes": porcentaje_imagenes,
        "porcentaje_descripciones": porcentaje_descripciones,
    }

    return render(request, "catalogo/admin/dashboard.html", context)


class ProductosCatalogoView(LoginRequiredMixin, ListView):

    model = ProductoCatalogo

    template_name = "catalogo/admin/productos_catalogo.html"

    context_object_name = "productos_catalogo"

    paginate_by = 30

    def get_queryset(self):

        queryset = (
            ProductoCatalogo.objects
            .select_related(
                "producto",
                "producto__familia",
                "producto__proveedor"
            )
        )

        q = self.request.GET.get(
            "q",
            ""
        ).strip()

        filtro = self.request.GET.get(
            "estado",
            ""
        )

        if q:

            queryset = queryset.filter(
                Q(producto__codigo__icontains=q)
                |
                Q(producto__titulo__icontains=q)
            )

        if filtro == "sin_foto":

            queryset = queryset.filter(
                Q(producto__imagen__isnull=True)
                |
                Q(producto__imagen="")
            )

        elif filtro == "sin_descripcion":

            queryset = queryset.filter(
                Q(descripcion_catalogo__isnull=True)
                |
                Q(descripcion_catalogo="")
            )

        return queryset.order_by(
            "producto__titulo"
        )


from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .forms import ProductoCatalogoForm


class ProductoCatalogoUpdateView(LoginRequiredMixin, UpdateView):

    model = ProductoCatalogo

    form_class = ProductoCatalogoForm

    template_name = "catalogo/admin/producto_editar.html"

    success_url = reverse_lazy("productos_catalogo")
