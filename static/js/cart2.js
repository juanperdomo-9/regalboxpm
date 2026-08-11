// ===========================================
// REGALBOX
// CART
// ===========================================

document.addEventListener("DOMContentLoaded", () => {
    initCart();
});

// ===========================================
// INIT
// ===========================================

let cartDrawer;
let cartOverlay;

function initCart() {

    cartDrawer = document.getElementById("cartDrawer");
    cartOverlay = document.getElementById("cartOverlay");

    document
        .getElementById("openCart")
        ?.addEventListener("click", openCart);

    document
        .getElementById("closeCart")
        ?.addEventListener("click", closeCart);

    cartOverlay?.addEventListener("click", closeCart);

    document.addEventListener("keydown", (e) => {

        if (e.key === "Escape") {

            closeCart();

        }

    });

    document
        .getElementById("checkoutButton")
        ?.addEventListener("click", () => {

            window.location.href = "/checkout/";

        });

    loadCart();

}

// ===========================================
// OPEN
// ===========================================

function openCart() {

    if (!cartDrawer || !cartOverlay) return;

    cartOverlay.classList.remove("hidden");

    requestAnimationFrame(() => {

        cartOverlay.classList.remove("opacity-0");

        cartDrawer.style.transform = "translateX(0)";

    });

    document.body.classList.add("overflow-hidden");

}

// ===========================================
// CLOSE
// ===========================================

function closeCart() {

    if (!cartDrawer || !cartOverlay) return;

    cartOverlay.classList.add("opacity-0");

    cartDrawer.style.transform = "translateX(100%)";

    setTimeout(() => {

        cartOverlay.classList.add("hidden");

    }, 300);

    document.body.classList.remove("overflow-hidden");

}

// ===========================================
// LOAD
// ===========================================

async function loadCart() {

    const response = await fetch("/cart/json/");

    const data = await response.json();

    renderCart(data);

}

// ===========================================
// RENDER
// ===========================================

function renderCart(data) {

    // contador

    document.querySelectorAll(".cart-count").forEach(counter => {

        counter.textContent = data.count;

        counter.animate(
            [
                { transform: "scale(1)" },
                { transform: "scale(1.25)" },
                { transform: "scale(1)" }
            ],
            {
                duration: 220
            }
        );

    });

    // total

    const total = document.getElementById("cartTotal");

    if (total) {

        total.textContent = "$" + data.total;

    }

    // contenedor

    const container = document.getElementById("cartItems");

    if (!container) return;

    container.innerHTML = "";

    // vacío

    if (data.items.length === 0) {

        container.innerHTML = `

            <div class="flex h-full flex-col items-center justify-center text-center">

                <div class="mb-6 text-6xl">
                    🛒
                </div>

                <h3 class="text-3xl font-semibold">

                    Tu carrito está vacío

                </h3>

                <p class="mt-3 text-zinc-500">

                    Agregá una Box para comenzar.

                </p>

            </div>

        `;

        return;

    }

    // productos

    data.items.forEach((item, index) => {

        container.innerHTML += `

            <div class="cart-item flex gap-5 border-b border-[#ECE8E3] py-6">

                <img
                    src="${item.image}"
                    class="h-24 w-24 rounded-2xl object-cover">

                <div class="flex flex-1 flex-col">

                        <h3 class="font-semibold">
                            ${item.name}
                        </h3>

                        ${item.dedication ? `
                            <p class="mt-2 text-sm italic text-[#9E3949]">
                                💌 ${item.dedication}
                            </p>
                        ` : ""}

                        <p class="mt-2 text-zinc-500">
                            $${item.price}
                        </p>

                    <div class="mt-5 flex items-center justify-between">

                        <div class="flex items-center gap-2 rounded-full border border-[#ECE8E3] px-2 py-1">

                            <button
                                class="cart-decrease h-8 w-8 rounded-full hover:bg-zinc-100"
                                data-id="${item.id}">

                                −

                            </button>

                            <span class="font-semibold">

                                ${item.quantity}

                            </span>

                            <button
                                class="cart-increase h-8 w-8 rounded-full hover:bg-zinc-100"
                                data-id="${item.id}">

                                +

                            </button>

                        </div>

                        <button
                            class="cart-remove text-zinc-400 hover:text-red-500"
                            data-id="${item.id}">

                            🗑

                        </button>

                    </div>

                </div>

            </div>

        `;

        container.lastElementChild.animate(
            [
                {
                    opacity: 0,
                    transform: "translateX(30px)"
                },
                {
                    opacity: 1,
                    transform: "translateX(0)"
                }
            ],
            {
                duration: 220 + index * 60,
                easing: "ease-out"
            }
        );

    });

}
// ===========================================
// UPDATE
// ===========================================

async function updateCart(id, quantity) {

    if (quantity <= 0) {
        return removeCart(id);
    }

    const formData = new FormData();

    formData.append("quantity", quantity);

    const response = await fetch(`/cart/update/${id}/`, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    });

    const data = await response.json();

    renderCart(data);

}

// ===========================================
// REMOVE
// ===========================================

async function removeCart(id) {

    const response = await fetch(`/cart/remove/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    });

    const data = await response.json();

    renderCart(data);

}

// ===========================================
// INCREASE
// ===========================================

function increaseCart(id, quantity) {

    updateCart(id, quantity + 1);

}

// ===========================================
// DECREASE
// ===========================================

function decreaseCart(id, quantity) {

    updateCart(id, quantity - 1);

}

// ===========================================
// EVENTS
// ===========================================

document.addEventListener("click", function (e) {

    const plus = e.target.closest(".cart-increase");

    if (plus) {

        const quantity = Number(
            plus.parentElement.querySelector("span").textContent
        );

        increaseCart(
            plus.dataset.id,
            quantity
        );

        return;

    }

    const minus = e.target.closest(".cart-decrease");

    if (minus) {

        const quantity = Number(
            minus.parentElement.querySelector("span").textContent
        );

        decreaseCart(
            minus.dataset.id,
            quantity
        );

        return;

    }

    const remove = e.target.closest(".cart-remove");

    if (remove) {

        removeCart(remove.dataset.id);

    }

});

// ===========================================
// HELPERS
// ===========================================

function getCSRFToken() {

    return document.querySelector("[name=csrfmiddlewaretoken]")?.value
        || getCookie("csrftoken");

}

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

            }

        }

    }

    return cookieValue;

}

// ===========================================
// PUBLIC
// ===========================================

window.openCart = openCart;
window.closeCart = closeCart;
window.loadCart = loadCart;
window.renderCart = renderCart;