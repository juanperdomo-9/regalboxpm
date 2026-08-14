import datetime

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import Avg, Count, Sum
from django.utils import timezone
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


# ==========================================================
# ADMIN SITE — branding + dashboard de métricas
# ==========================================================

class RegalboxPmAdminSite(admin.AdminSite):

    site_header = "REGALBOX PM"
    site_title = "REGALBOX PM Admin"
    index_title = "Panel de control"

    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context["dashboard"] = self._build_dashboard()

        return super().index(request, extra_context)

    def _build_dashboard(self):

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - datetime.timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)

        orders_qs = Order.objects.exclude(status="cancelled")

        total_revenue = orders_qs.aggregate(total=Sum("total"))["total"] or 0
        avg_order = orders_qs.aggregate(avg=Avg("total"))["avg"] or 0

        counts_map = {
            row["status"]: row["count"]
            for row in Order.objects.values("status").annotate(count=Count("id"))
        }

        status_counts = [
            {"value": value, "label": label, "count": counts_map.get(value, 0)}
            for value, label in Order.STATUS_CHOICES
        ]

        top_boxes = (
            OrderItem.objects
            .values("gift_box__name")
            .annotate(total_qty=Sum("quantity"))
            .order_by("-total_qty")[:5]
        )

        low_stock = (
            GiftBox.objects
            .filter(active=True, unlimited_stock=False, stock__lte=5)
            .order_by("stock")[:8]
        )

        recent_orders = Order.objects.order_by("-created_at")[:8]

        return {
            "total_revenue": total_revenue,
            "avg_order": avg_order,
            "orders_today": Order.objects.filter(created_at__gte=today_start).count(),
            "orders_week": Order.objects.filter(created_at__gte=week_start).count(),
            "orders_month": Order.objects.filter(created_at__gte=month_start).count(),
            "status_counts": status_counts,
            "top_boxes": top_boxes,
            "low_stock": low_stock,
            "recent_orders": recent_orders,
        }


admin_site = RegalboxPmAdminSite(name="admin")

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


STATUS_COLORS = {
    "pending": ("#FFF4CC", "#8A6D00"),
    "paid": ("#D9F2E3", "#127A3E"),
    "preparing": ("#E1E9FF", "#2C4EBD"),
    "sent": ("#E4D9FF", "#5B21B6"),
    "delivered": ("#D4F4DD", "#0F6B33"),
    "cancelled": ("#FBD9D9", "#9B1C1C"),
}


# ==========================================================
# CATEGORY
# ==========================================================

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "slug",
        "order",
        "active",
        "coming_soon",
    )

    list_editable = (
        "order",
        "active",
        "coming_soon",
    )

    list_filter = (
        "active",
        "coming_soon",
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


# ==========================================================
# OCCASION
# ==========================================================

@admin.register(Occasion, site=admin_site)
class OccasionAdmin(admin.ModelAdmin):

    list_display = (
        "icon",
        "name",
        "slug",
        "order",
        "active",
    )

    list_editable = (
        "order",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# ==========================================================
# GIFT ITEM
# ==========================================================

@admin.register(GiftItem, site=admin_site)
class GiftItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "short_description",
        "active",
    )

    list_editable = (
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
    )

    def short_description(self, obj):
        return (obj.description[:60] + "…") if len(obj.description) > 60 else obj.description

    short_description.short_description = "Descripción"


# ==========================================================
# INLINES
# ==========================================================

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

    autocomplete_fields = (
        "item",
    )


# ==========================================================
# GIFT BOX
# ==========================================================

@admin.register(GiftBox, site=admin_site)
class GiftBoxAdmin(admin.ModelAdmin):

    date_hierarchy = "created_at"

    list_display = (
        "image_preview",
        "name",
        "category",
        "price",
        "stock_display",
        "featured",
        "active",
    )

    list_filter = (
        "category",
        "featured",
        "active",
        "unlimited_stock",
        "personalized",
    )

    search_fields = (
        "name",
        "sku",
    )

    list_editable = (
        "price",
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
                    "unlimited_stock",
                    "display_order",
                    "featured",
                    "personalized",
                    "active",
                )
            },
        ),

        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": (
                    "meta_title",
                    "meta_description",
                ),
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

    def stock_display(self, obj):

        if obj.unlimited_stock:
            return format_html('<span style="color:#127A3E;font-weight:600;">{}</span>', "Ilimitado")

        if obj.stock <= 0:
            return format_html('<span style="color:#9B1C1C;font-weight:600;">{}</span>', "Sin stock")

        if obj.stock <= 5:
            return format_html('<span style="color:#C60018;font-weight:600;">{} u.</span>', obj.stock)

        return f"{obj.stock} u."

    stock_display.short_description = "Stock"
    stock_display.admin_order_field = "stock"


# ==========================================================
# DELIVERY ZONE
# ==========================================================

@admin.register(DeliveryZone, site=admin_site)
class DeliveryZoneAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "estimated_days",
        "display_order",
        "active",
    )

    list_editable = (
        "price",
        "display_order",
        "active",
    )


# ==========================================================
# ORDER ITEM INLINE
# ==========================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    fields = (
        "gift_box",
        "quantity",
        "price",
        "subtotal_display",
        "dedication",
    )

    readonly_fields = (
        "gift_box",
        "quantity",
        "price",
        "subtotal_display",
    )

    can_delete = False

    def subtotal_display(self, obj):
        return f"${obj.subtotal}" if obj.pk else "-"

    subtotal_display.short_description = "Subtotal"


# ==========================================================
# ORDER ACTIONS
# ==========================================================

@admin.action(description="Marcar como pagado")
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(status="paid")


@admin.action(description="Marcar como preparando")
def mark_as_preparing(modeladmin, request, queryset):
    queryset.update(status="preparing")


@admin.action(description="Marcar como enviado")
def mark_as_sent(modeladmin, request, queryset):
    queryset.update(status="sent")


@admin.action(description="Marcar como entregado")
def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(status="delivered")


# ==========================================================
# ORDER
# ==========================================================

@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):

    date_hierarchy = "created_at"

    list_display = (
        "code",
        "full_name",
        "city",
        "status_badge",
        "total_items_display",
        "total",
        "created_at",
    )

    list_filter = (
        "status",
        "city",
        "delivery_method",
        "created_at",
    )

    search_fields = (
        "code",
        "full_name",
        "address",
    )

    readonly_fields = (
        "code",
        "subtotal",
        "shipping_cost",
        "total",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Pedido",
            {
                "fields": (
                    "code",
                    "status",
                    "created_at",
                )
            },
        ),

        (
            "Cliente",
            {
                "fields": (
                    "full_name",
                    "city",
                    "address",
                    "notes",
                )
            },
        ),

        (
            "Totales",
            {
                "fields": (
                    "subtotal",
                    "shipping_cost",
                    "total",
                )
            },
        ),

        (
            "Envío / seguimiento",
            {
                "classes": ("collapse",),
                "fields": (
                    "delivery_method",
                    "delivery_zone",
                    "tracking_number",
                    "paid_at",
                    "delivered_at",
                ),
            },
        ),

    )

    inlines = [
        OrderItemInline,
    ]

    actions = [
        mark_as_paid,
        mark_as_preparing,
        mark_as_sent,
        mark_as_delivered,
    ]

    def status_badge(self, obj):

        bg, fg = STATUS_COLORS.get(obj.status, ("#eee", "#333"))

        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;'
            'border-radius:999px;font-size:11px;font-weight:600;'
            'white-space:nowrap;">{}</span>',
            bg, fg, obj.get_status_display(),
        )

    status_badge.short_description = "Estado"
    status_badge.admin_order_field = "status"

    def total_items_display(self, obj):
        return obj.total_items

    total_items_display.short_description = "Unidades"


# ==========================================================
# GIFT BOX IMAGE
# ==========================================================

@admin.register(GiftBoxImage, site=admin_site)
class GiftBoxImageAdmin(admin.ModelAdmin):

    list_display = (
        "preview",
        "gift_box",
        "order",
    )

    list_filter = (
        "gift_box",
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
