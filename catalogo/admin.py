from django.contrib import admin

from .models import (
    Producto,
    Familia,
    Proveedor,
    ProductoGrupo,
    ProductoMedida
)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'titulo',
        'proveedor',
        'familia',
        'stock',
        'habilitado'
    )

    list_filter = (
        'familia',
        'proveedor',
        'habilitado'
    )

    search_fields = (
        'codigo',
        'titulo',
        'proveedor__marca'
    )

    ordering = (
        'titulo',
    )

    list_per_page = 50


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'titulo'
    )

    search_fields = (
        'codigo',
        'titulo'
    )


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'marca',
        'razon_social'
    )

    search_fields = (
        'codigo',
        'marca',
        'razon_social'
    )


@admin.register(ProductoGrupo)
class ProductoGrupoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre'
    )


@admin.register(ProductoMedida)
class ProductoMedidaAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'descripcion'
    )