from django.urls import path

from .views import (
    CatalogoView,
    ProductoDetalleView,
    dashboard_catalogo,
    login_catalogo,
    logout_catalogo,
    ProductosCatalogoView,
    ProductoCatalogoUpdateView,
)

urlpatterns = [
    # PUBLICO
    path("", CatalogoView.as_view(), name="catalogo"),
    path("producto/<int:id>/", ProductoDetalleView.as_view(), name="detalle_producto"),
    # LOGIN
    path("login/", login_catalogo, name="login_catalogo"),
    path("logout/", logout_catalogo, name="logout_catalogo"),
    # ADMIN
    path("catalogo-admin/", dashboard_catalogo, name="dashboard_catalogo"),
    path(
        "catalogo-admin/productos/",
        ProductosCatalogoView.as_view(),
        name="productos_catalogo",
    ),
    path(
        "catalogo-admin/producto/<int:pk>/editar/",
        ProductoCatalogoUpdateView.as_view(),
        name="editar_producto_catalogo",
    ),
]
