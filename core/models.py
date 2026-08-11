from django.db import models
from django.utils.text import slugify


# =====================================================
# CATEGORÍAS
# =====================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/",
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================================================
# OCASIONES
# =====================================================

class Occasion(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    icon = models.CharField(
        max_length=50,
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Ocasión"
        verbose_name_plural = "Ocasiones"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================================================
# PRODUCTOS INDIVIDUALES
# =====================================================

class GiftItem(models.Model):

    name = models.CharField(
        max_length=150
    )

    image = models.ImageField(
        upload_to="gift-items/",
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Producto de Caja"
        verbose_name_plural = "Productos de Caja"

    def __str__(self):
        return self.name

# =====================================================
# GIFT BOXES
# =====================================================

class GiftBox(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="boxes"
    )

    occasions = models.ManyToManyField(
        Occasion,
        blank=True,
        related_name="boxes"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    sku = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True
    )

    short_description = models.CharField(
        max_length=250
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="gift-boxes/",
        max_length=255
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    unlimited_stock = models.BooleanField(
        default=False,
        verbose_name="Stock ilimitado"
    )

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text="Peso en Kg"
    )

    featured = models.BooleanField(
        default=False
    )

    personalized = models.BooleanField(
        default=False,
        verbose_name="Permite dedicatoria"
    )

    active = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    meta_title = models.CharField(
        max_length=70,
        blank=True
    )

    meta_description = models.CharField(
        max_length=160,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "display_order",
            "-featured",
            "name"
        ]
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        if not self.sku:
            self.sku = self.slug.upper().replace("-", "")[:12]

        super().save(*args, **kwargs)

    @property
    def has_stock(self):
        return self.unlimited_stock or self.stock > 0

    def __str__(self):
        return self.name

# =====================================================
# IMÁGENES DE LAS BOXES
# =====================================================

class GiftBoxImage(models.Model):

    gift_box = models.ForeignKey(
        GiftBox,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="gift-boxes/gallery/",
        max_length=255
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Imagen de Caja"
        verbose_name_plural = "Imágenes de Caja"

    def __str__(self):
        return f"Imagen de {self.gift_box.name}"


# =====================================================
# PRODUCTOS DE CADA BOX
# =====================================================

class GiftBoxItem(models.Model):

    gift_box = models.ForeignKey(
        GiftBox,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        GiftItem,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    optional = models.BooleanField(
        default=False,
        verbose_name="Producto opcional"
    )

    class Meta:
        verbose_name = "Contenido de Caja"
        verbose_name_plural = "Contenidos de Caja"

    def __str__(self):
        return f"{self.quantity} × {self.item.name}"


# =====================================================
# ZONAS DE ENVÍO
# =====================================================

class DeliveryZone(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    estimated_days = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Tiempo estimado"
    )

    active = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Zona de Envío"
        verbose_name_plural = "Zonas de Envío"

    def __str__(self):
        return self.name

# =====================================================
# PEDIDOS
# =====================================================

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("paid", "Pagado"),
        ("preparing", "Preparando"),
        ("sent", "Enviado"),
        ("delivered", "Entregado"),
        ("cancelled", "Cancelado"),
    ]

    DELIVERY_CHOICES = [
        ("delivery", "Envío a domicilio"),
        ("pickup", "Retiro por el local"),
    ]

    code = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    address = models.CharField(
        max_length=250,
        blank=True
    )

    city = models.CharField(
        max_length=100
    )

    postal_code = models.CharField(
        max_length=15,
        blank=True
    )

    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default="delivery"
    )

    notes = models.TextField(
        blank=True
    )

    delivery_zone = models.ForeignKey(
        DeliveryZone,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    preference_id = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    tracking_number = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return self.code


# =====================================================
# PRODUCTOS DEL PEDIDO
# =====================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    gift_box = models.ForeignKey(
        GiftBox,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    dedication = models.TextField(
        blank=True,
        default="",
        verbose_name="Dedicatoria"
    )

    class Meta:
        verbose_name = "Producto del Pedido"
        verbose_name_plural = "Productos del Pedido"

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.gift_box.name} x{self.quantity}"