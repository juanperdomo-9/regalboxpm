from decimal import Decimal

from .models import GiftBox


class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get("cart")

        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

        valid_ids = set(
            str(pk)
            for pk in GiftBox.objects.values_list("id", flat=True)
        )

        self.cart = {
            pk: value
            for pk, value in self.cart.items()
            if pk in valid_ids
        }

        self.session["cart"] = self.cart
        self.save()

    def add(self, gift_box, quantity=1, dedication=""):

        product_id = str(gift_box.id)

        quantity = int(quantity)

        if product_id not in self.cart:

            self.cart[product_id] = {
                "quantity": quantity,
                "dedication": dedication.strip()
            }

        else:

            self.cart[product_id]["quantity"] += quantity

            # Si escribe una nueva dedicatoria la reemplaza
            if dedication.strip():

                self.cart[product_id]["dedication"] = dedication.strip()

        self.save()

    def remove(self, gift_box):

        product_id = str(gift_box.id)

        if product_id in self.cart:

            del self.cart[product_id]

            self.save()

    def decrease(self, gift_box):

        product_id = str(gift_box.id)

        if product_id in self.cart:

            self.cart[product_id]["quantity"] -= 1

            if self.cart[product_id]["quantity"] <= 0:

                del self.cart[product_id]

            self.save()

    def update(self, gift_box, quantity):

        product_id = str(gift_box.id)

        quantity = int(quantity)

        if product_id in self.cart:

            self.cart[product_id]["quantity"] = quantity

            if quantity <= 0:

                del self.cart[product_id]

            self.save()

    def clear(self):

        self.session["cart"] = {}

        self.save()

    def save(self):

        self.session.modified = True

    def __len__(self):

        return sum(item["quantity"] for item in self.cart.values())

    def get_total(self):

        total = Decimal("0")

        for item in self.items():

            total += item["subtotal"]

        return total

    def items(self):

        items = []

        for product_id, data in self.cart.items():

            try:

                product = GiftBox.objects.get(pk=int(product_id))

                quantity = data["quantity"]

                items.append({

                    "product": product,

                    "quantity": quantity,

                    "subtotal": product.price * quantity,

                    "dedication": data.get("dedication", "")

                })

            except GiftBox.DoesNotExist:

                continue

        return items