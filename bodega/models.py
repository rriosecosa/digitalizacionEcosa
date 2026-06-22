from django.db import models

# Create your models here.
from django.db import models

class BodegaDocumentoF8(models.Model):
    ESTADOS_F8 = [
        ('PENDIENTE', 'Pendiente de Picking'),
        ('EN_PICKING', 'En Proceso de Picking'),
        ('LISTO', 'Listo para Empaque'),
        ('PROCESADO', 'Procesado y Terminado'),
    ]
    
    BODEGAS = [
        ('01', 'ECOSA'),
        ('02', 'TRUPER'),
    ]

    # Vinculamos al N° de Nota de Venta existente en tu app de ventas
    # Si tu modelo de Nota Venta está en otra app, cambia 'ventas.NotaVenta' por la app correspondiente
    nota_venta_numero = models.ForeignKey('ventas.NotaVenta', on_delete=models.CASCADE, related_name='documentos_f8')
    bodega_codigo = models.CharField(max_length=2, choices=BODEGAS)
    estado = models.CharField(max_length=20, choices=ESTADOS_F8, default='PENDIENTE')
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"F8-{self.id} | Bodega {self.get_bodega_codigo_display()} | Nota: {self.nota_venta_numero}"

class BodegaProductoCodigoBarra(models.Model):
    TIPOS_EMPAQUE = [
        ('INDIVIDUAL', 'Individual (1 u)'),
        ('INNER', 'Inner (Paquete Intermedio)'),
        ('MASTER', 'Master (Caja Proveedor)'),
    ]

    # Vinculamos al Producto existente de tu catálogo web
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='codigos_barra')
    codigo_barra_valor = models.CharField(max_length=100, unique=True, db_index=True)
    tipo_empaque = models.CharField(max_length=15, choices=TIPOS_EMPAQUE, default='INDIVIDUAL')
    unidades_equivalencia = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.codigo_barra_valor} ({self.tipo_empaque} -> {self.unidades_equivalencia} u)"