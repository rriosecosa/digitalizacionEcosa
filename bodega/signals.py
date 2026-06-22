from django.db.models.signals import post_save
from django.dispatch import receiver
from ventas.models import NotaVenta, LineaNotaVenta
from bodega.models import BodegaDocumentoF8

@receiver(post_save, sender=NotaVenta)
def separar_nota_venta_por_bodega(sender, instance, created, **kwargs):
    # Trigger: Solo actuamos si la ejecutiva cambia el estado a 'ENVIADO_A_BODEGA'
    if instance.estado == 'ENVIADO_A_BODEGA':
        lineas = LineaNotaVenta.objects.filter(n_nota_venta=instance)
        
        tiene_ecosa = False
        tiene_truper = False
        
        for linea in lineas:
            # Analizamos la regla del ID del producto ("X1-X2-X3")
            # Separamos por el guion para obtener X1 (ID Proveedor)
            partes_id = linea.codigo_producto.split('-')
            if partes_id:
                id_proveedor = partes_id[0] # Captura el '01', '02', etc.
                
                if id_proveedor == '02':
                    tiene_truper = True
                else:
                    tiene_ecosa = True

        # Creamos las órdenes de preparación en paralelo por cada bodega involucrada
        if tiene_ecosa:
            BodegaDocumentoF8.objects.get_or_create(
                nota_venta_numero=instance,
                bodega_codigo='01'
            )
        if tiene_truper:
            BodegaDocumentoF8.objects.get_or_create(
                nota_venta_numero=instance,
                bodega_codigo='02'
            )