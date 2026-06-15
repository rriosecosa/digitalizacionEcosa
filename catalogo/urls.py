from django.urls import path
from .views import CatalogoView, ProductoDetalleView

urlpatterns = [

    path(
        '',
        CatalogoView.as_view(),
        name='catalogo'
    ),

    path(
        'producto/<int:id>/',
        ProductoDetalleView.as_view(),
        name='detalle_producto'
    ),

]