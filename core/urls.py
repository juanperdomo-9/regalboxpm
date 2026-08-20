from django.urls import path

from . import views

urlpatterns = [

    # ==========================
    # HOME
    # ==========================

    path(
        "",
        views.home,
        name="home"
    ),

    # ==========================
    # CATEGORIES
    # ==========================

    path(
        "categoria/<slug:slug>/",
        views.category_detail,
        name="category_detail"
    ),

    # ==========================
    # PRODUCT DETAIL
    # ==========================

    path(
        "box/<slug:slug>/",
        views.giftbox_detail,
        name="giftbox_detail"
    ),

    # ==========================
    # CART
    # ==========================

    path(
        "cart/add/<int:pk>/",
        views.cart_add,
        name="cart_add",
    ),

    path(
        "cart/remove/<int:pk>/",
        views.cart_remove,
        name="cart_remove",
    ),

    path(
        "cart/decrease/<int:pk>/",
        views.cart_decrease,
        name="cart_decrease",
    ),

    path(
        "cart/update/<int:pk>/",
        views.cart_update,
        name="cart_update",
    ),

    path(
        "cart/clear/",
        views.cart_clear,
        name="cart_clear",
    ),

    path(
        "cart/json/",
        views.cart_json,
        name="cart_json",
    ),

    # ==========================
    # CHECKOUT
    # ==========================

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    path(
        "checkout/create/",
        views.checkout_create,
        name="checkout_create",
    ),

    # ==========================
    # GIFT FINDER (IA)
    # ==========================

    path(
        "gift-finder/chat/",
        views.gift_finder_chat,
        name="gift_finder_chat",
    ),

    path(
        "gift-finder/reset/",
        views.gift_finder_reset,
        name="gift_finder_reset",
    ),

    path(
        "gift-finder/history/",
        views.gift_finder_history,
        name="gift_finder_history",
    ),
]