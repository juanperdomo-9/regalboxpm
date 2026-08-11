from urllib.parse import quote

from django.conf import settings
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from .gift_finder import run_gift_finder_turn
from .models import Category, GiftBox, Order, OrderItem


# ==========================================================
# HOME
# ==========================================================

def home(request):

    featured_boxes = (
        GiftBox.objects
        .filter(active=True, featured=True)
        .select_related("category")
        .prefetch_related("images")
        .order_by("-created_at")
    )

    latest_boxes = (
        GiftBox.objects
        .filter(active=True)
        .select_related("category")
        .order_by("-created_at")[:8]
    )

    categories = (
        Category.objects
        .prefetch_related("boxes")
        .all()
    )

    return render(
        request,
        "home.html",
        {
            "featured_boxes": featured_boxes,
            "latest_boxes": latest_boxes,
            "categories": categories,
        },
    )


# ==========================================================
# CATEGORY
# ==========================================================

def category_detail(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug,
    )

    boxes = (
        category.boxes
        .filter(active=True)
        .select_related("category")
        .prefetch_related(
            "images",
            "items__item",
            "occasions",
        )
    )

    return render(
        request,
        "category.html",
        {
            "category": category,
            "boxes": boxes,
        },
    )


# ==========================================================
# GIFTBOX DETAIL
# ==========================================================

def giftbox_detail(request, slug):

    giftbox = get_object_or_404(
        GiftBox.objects
        .select_related("category")
        .prefetch_related(
            "images",
            "items__item",
            "occasions",
        ),
        slug=slug,
        active=True,
    )

    related_boxes = (
        GiftBox.objects
        .filter(
            category=giftbox.category,
            active=True,
        )
        .exclude(pk=giftbox.pk)
        .select_related("category")
        .prefetch_related("images")
        [:3]
    )

    return render(
        request,
        "giftbox.html",
        {
            "giftbox": giftbox,
            "related_boxes": related_boxes,
        },
    )


# ==========================================================
# CART
# ==========================================================

def cart_response(cart, extra=None):

    payload = {

        "success": True,

        "count": len(cart),

        "total": str(cart.get_total()),

        "items": [

            {

                "pk": item["product"].id,

                "id": item["product"].id,

                "name": item["product"].name,

                "price": str(item["product"].price),

                "quantity": item["quantity"],

                "dedication": item["dedication"],

                "image": item["product"].image.url
                if item["product"].image
                else ""

            }

            for item in cart.items()

        ]

    }

    if extra:
        payload.update(extra)

    return JsonResponse(payload)


# ==========================================================
# ADD
# ==========================================================

def cart_add(request, pk):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400
        )

    cart = Cart(request)

    giftbox = get_object_or_404(
        GiftBox,
        pk=pk,
        active=True,
    )

    if not giftbox.has_stock:

        return JsonResponse(
            {
                "success": False,
                "error": f"{giftbox.name} no tiene stock disponible en este momento.",
            },
            status=400,
        )

    quantity = int(request.POST.get("quantity", 1))
    dedication = request.POST.get("dedication", "")

    warning = None

    if not giftbox.unlimited_stock:

        current_qty = cart.cart.get(str(giftbox.id), {}).get("quantity", 0)
        available = giftbox.stock - current_qty

        if available <= 0:

            return JsonResponse(
                {
                    "success": False,
                    "error": f"Ya tenés en el carrito todo el stock disponible de {giftbox.name}.",
                },
                status=400,
            )

        if quantity > available:

            quantity = available
            warning = f"Solo quedaban {available} unidad(es) de {giftbox.name}, ajustamos la cantidad."

    cart.add(
        gift_box=giftbox,
        quantity=quantity,
        dedication=dedication
    )

    extra = {"warning": warning} if warning else None

    return cart_response(cart, extra=extra)


# ==========================================================
# REMOVE
# ==========================================================

def cart_remove(request, pk):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400
        )

    cart = Cart(request)

    giftbox = get_object_or_404(
        GiftBox,
        pk=pk,
    )

    cart.remove(giftbox)

    return cart_response(cart)


# ==========================================================
# DECREASE
# ==========================================================

def cart_decrease(request, pk):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400
        )

    cart = Cart(request)

    giftbox = get_object_or_404(
        GiftBox,
        pk=pk,
    )

    cart.decrease(giftbox)

    return cart_response(cart)


# ==========================================================
# UPDATE
# ==========================================================

def cart_update(request, pk):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400
        )

    cart = Cart(request)

    giftbox = get_object_or_404(
        GiftBox,
        pk=pk,
    )

    quantity = int(request.POST.get("quantity", 1))

    if not giftbox.unlimited_stock and quantity > giftbox.stock:
        quantity = giftbox.stock

    cart.update(
        gift_box=giftbox,
        quantity=quantity,
    )

    return cart_response(cart)


# ==========================================================
# CLEAR
# ==========================================================

def cart_clear(request):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400
        )

    cart = Cart(request)

    cart.clear()

    return cart_response(cart)


# ==========================================================
# JSON
# ==========================================================

def cart_json(request):

    cart = Cart(request)

    return cart_response(cart)


# ==========================================================
# CHECKOUT
# ==========================================================

def checkout(request):

    cart = Cart(request)

    return render(
        request,
        "checkout.html",
        {
            "cart": cart,
            "items": cart.items(),
            "total": cart.get_total(),
            "cart_empty": len(cart) == 0,
        },
    )


def checkout_create(request):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400
        )

    cart = Cart(request)
    items = cart.items()

    if len(items) == 0:

        return JsonResponse(
            {"success": False, "error": "Tu carrito está vacío."},
            status=400,
        )

    full_name = request.POST.get("full_name", "").strip()
    city = request.POST.get("city", "").strip()
    address = request.POST.get("address", "").strip()
    notes = request.POST.get("notes", "").strip()

    if not full_name or not city or not address:

        return JsonResponse(
            {
                "success": False,
                "error": "Completá nombre, origen y ubicación para poder coordinar el envío.",
            },
            status=400,
        )

    # El stock pudo cambiar desde que se agregó al carrito
    # (otro pedido, o un ajuste manual desde el admin).

    for item in items:

        gift_box = item["product"]

        if not gift_box.unlimited_stock and item["quantity"] > gift_box.stock:

            return JsonResponse(
                {
                    "success": False,
                    "error": f"Solo quedan {gift_box.stock} unidad(es) de {gift_box.name}. Ajustá tu carrito para continuar.",
                },
                status=400,
            )

    subtotal = cart.get_total()

    with transaction.atomic():

        order = Order.objects.create(
            code="TEMP",
            full_name=full_name,
            email="",
            phone="",
            address=address,
            city=city,
            notes=notes,
            delivery_zone=None,
            subtotal=subtotal,
            shipping_cost=0,
            total=subtotal,
            status="pending",
        )

        order.code = f"RB-{order.id + settings.ORDER_CODE_OFFSET:06d}"
        order.save(update_fields=["code"])

        for item in items:

            gift_box = item["product"]

            OrderItem.objects.create(
                order=order,
                gift_box=gift_box,
                quantity=item["quantity"],
                price=gift_box.price,
                dedication=item["dedication"],
            )

            if not gift_box.unlimited_stock:

                gift_box.stock = max(gift_box.stock - item["quantity"], 0)
                gift_box.save(update_fields=["stock"])

    whatsapp_url = build_whatsapp_url(order, items)

    cart.clear()

    return JsonResponse({
        "success": True,
        "code": order.code,
        "whatsapp_url": whatsapp_url,
    })


def build_whatsapp_url(order, items):

    lines = [
        "¡Hola REGALBOXX! 👋🎁",
        "",
        "Quiero hacer un pedido ✨",
        "",
        f"🧾 Pedido: #{order.code}",
        "",
        "👤 Nombre:",
        order.full_name,
        "",
        "📍 Origen:",
        order.city,
        "",
        "🗺️ Ubicación:",
        order.address,
    ]

    for item in items:

        lines.append("")
        lines.append("🎁 Box:")
        lines.append(f"{item['product'].name} x{item['quantity']}")

        if item["dedication"]:
            lines.append("💌 Dedicatoria:")
            lines.append(item["dedication"])

    lines.append("")
    lines.append("💰 Subtotal:")
    lines.append(f"${order.subtotal}")

    if order.notes:
        lines.append("")
        lines.append("📝 Notas:")
        lines.append(order.notes)

    lines.append("")
    lines.append("Quisiera coordinar el pago y el envío 😊🚚")

    message = "\n".join(lines)

    return f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(message)}"


# ==========================================================
# GIFT FINDER (IA)
# ==========================================================

GIFT_FINDER_SESSION_KEY = "gift_finder_history"
GIFT_FINDER_RECOMMENDED_KEY = "gift_finder_recommended"

GIFT_FINDER_LIMIT_REPLY = (
    "¡Charlamos bastante y me encantó ayudarte! 😊 Para cerrar los "
    "detalles y coordinar todo, seguime por WhatsApp así te atiendo mejor."
)


def gift_finder_chat(request):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400,
        )

    message = request.POST.get("message", "").strip()

    if not message:

        return JsonResponse(
            {"success": False, "error": "Escribime algo para poder ayudarte 🙂"},
            status=400,
        )

    history = request.session.get(GIFT_FINDER_SESSION_KEY, [])

    user_turns = sum(1 for turn in history if turn["role"] == "user")

    if user_turns >= settings.GIFT_FINDER_MAX_USER_TURNS:

        return JsonResponse({
            "success": True,
            "reply": GIFT_FINDER_LIMIT_REPLY,
            "recommended_box": None,
            "whatsapp_url": f"https://wa.me/{settings.WHATSAPP_NUMBER}",
            "limit_reached": True,
        })

    already_recommended = request.session.get(GIFT_FINDER_RECOMMENDED_KEY, False)

    result = run_gift_finder_turn(history, message, already_recommended)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": result["reply"]})

    request.session[GIFT_FINDER_SESSION_KEY] = history

    if result["recommended_box"]:
        request.session[GIFT_FINDER_RECOMMENDED_KEY] = True

    request.session.modified = True

    return JsonResponse({
        "success": True,
        "reply": result["reply"],
        "recommended_box": result["recommended_box"],
        "whatsapp_url": None,
        "limit_reached": False,
    })


def gift_finder_reset(request):

    if request.method != "POST":

        return JsonResponse(
            {"success": False},
            status=400,
        )

    request.session.pop(GIFT_FINDER_SESSION_KEY, None)
    request.session.pop(GIFT_FINDER_RECOMMENDED_KEY, None)
    request.session.modified = True

    return JsonResponse({"success": True})