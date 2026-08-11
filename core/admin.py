from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Occasion,
    GiftItem,
    GiftBox,
    GiftBoxImage,
    GiftBoxItem,
    DeliveryZone,
    Order,
    OrderItem,
)


# ============================
# CATEGORY
# ============================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:8px;">',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Imagen"


# ============================
# OCCASION
# ============================

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# ============================
# GIFT ITEM
# ============================

@admin.register(GiftItem)
class GiftItemAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
    )

    search_fields = (
        "name",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60">',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Imagen"


# ============================
# INLINES
# ============================

class GiftBoxImageInline(admin.TabularInline):

    model = GiftBoxImage

    extra = 1

    fields = (
        "image_preview",
        "image",
        "order",
    )

    readonly_fields = (
        "image_preview",
    )

    ordering = (
        "order",
    )

    def image_preview(self, obj):

        if obj.pk and obj.image:

            return format_html(
                '<img src="{}" style="height:90px;border-radius:10px;">',
                obj.image.url,
            )

        return "-"

    image_preview.short_description = "Vista previa"


class GiftBoxItemInline(admin.TabularInline):

    model = GiftBoxItem

    extra = 1


# ============================
# GIFT BOX
# ============================

@admin.register(GiftBox)
class GiftBoxAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "category",
        "price",
        "stock",
        "featured",
        "active",
    )

    list_filter = (
        "category",
        "featured",
        "active",
    )

    search_fields = (
        "name",
    )

    list_editable = (
        "price",
        "stock",
        "featured",
        "active",
    )

    filter_horizontal = (
        "occasions",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        GiftBoxImageInline,
        GiftBoxItemInline,
    ]

    fieldsets = (

        (
            "Información",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "occasions",
                )
            },
        ),

        (
            "Contenido",
            {
                "fields": (
                    "short_description",
                    "description",
                )
            },
        ),

        (
            "Imagen principal",
            {
                "fields": (
                    "image_preview",
                    "image",
                )
            },
        ),

        (
            "Venta",
            {
                "fields": (
                    "price",
                    "stock",
                    "featured",
                    "personalized",
                    "active",
                )
            },
        ),

    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" style="height:120px;border-radius:12px;">',
                obj.image.url,
            )

        return "-"

    image_preview.short_description = "Imagen principal"

# ============================
# DELIVERY ZONE
# ============================

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "active",
    )

    list_editable = (
        "price",
        "active",
    )


# ============================
# ORDER ITEM INLINE
# ============================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "gift_box",
        "quantity",
        "price",
    )

    can_delete = False


# ============================
# ORDER
# ============================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "full_name",
        "status",
        "total",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "code",
        "full_name",
        "email",
    )

    readonly_fields = (
        "subtotal",
        "shipping_cost",
        "total",
        "created_at",
    )

    inlines = [
        OrderItemInline,
    ]

@admin.register(GiftBoxImage)
class GiftBoxImageAdmin(admin.ModelAdmin):

    list_display = (
        "preview",
        "gift_box",
        "order",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "gift_box",
        "order",
    )

    def preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" style="height:70px;border-radius:8px;">',
                obj.image.url,
            )

        return "-"

    preview.short_description = "Imagen"