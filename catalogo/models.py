from django.db import models


class Familia(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    titulo = models.CharField(max_length=100, blank=True, null=True)
    alias = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "familias"
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo or "Sin nombre"


class Proveedor(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    codigo = models.CharField(max_length=30, blank=True, null=True)
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    alias = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "proveedores"
        ordering = ["marca"]

    def __str__(self):
        return self.marca or "Sin marca"


class ProductoGrupo(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "productos_grupo"

    def __str__(self):
        return self.nombre


class ProductoMedida(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "productos_medida"

    def __str__(self):
        return self.descripcion or ""


class Producto(models.Model):
    id = models.IntegerField(primary_key=True)

    codigo = models.CharField(max_length=30)

    titulo = models.CharField(max_length=100, blank=True, null=True)

    alias = models.CharField(max_length=200, blank=True, null=True)

    stock = models.IntegerField()

    imagen = models.CharField(max_length=200, blank=True, null=True)

    habilitado = models.IntegerField()

    receta = models.IntegerField()

    eliminado = models.IntegerField()

    historico = models.IntegerField()

    proveedor = models.ForeignKey(
        Proveedor,
        db_column="fk_id_prov",
        on_delete=models.DO_NOTHING,
        related_name="productos",
    )

    familia = models.ForeignKey(
        Familia,
        db_column="fk_id_fam",
        on_delete=models.DO_NOTHING,
        related_name="productos",
    )

    grupo = models.ForeignKey(
        ProductoGrupo,
        db_column="fk_id_grupo",
        on_delete=models.DO_NOTHING,
        related_name="productos",
    )

    medida = models.ForeignKey(
        ProductoMedida,
        db_column="fk_id_medida",
        on_delete=models.DO_NOTHING,
        related_name="productos",
    )

    class Meta:
        managed = False
        db_table = "productos"
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

    @property
    def imagen_url(self):

        if self.imagen:
            return f"/media/{self.imagen}"

        return "/static/images/producto-default.png"


class ProductoCatalogo(models.Model):

    producto = models.OneToOneField(
        Producto, on_delete=models.CASCADE, related_name="catalogo"
    )

    imagen_catalogo = models.ImageField(upload_to="catalogo/", blank=True, null=True)

    descripcion_catalogo = models.TextField(blank=True, null=True)

    especificaciones = models.TextField(blank=True, null=True)

    referencia = models.CharField(max_length=100, blank=True, null=True)

    orden_catalogo = models.IntegerField(default=0)

    visible_catalogo = models.BooleanField(default=True)

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["orden_catalogo", "producto__titulo"]

        verbose_name = "Producto Catálogo"
        verbose_name_plural = "Productos Catálogo"

    @property
    def imagen_final(self):

        if self.imagen_catalogo:
            return self.imagen_catalogo.url

        if self.producto.imagen:
            return f"/media/{self.producto.imagen}"

        return "/static/images/producto-default.png"

    def __str__(self):

        return f"{self.producto.codigo} - {self.producto.titulo}"
