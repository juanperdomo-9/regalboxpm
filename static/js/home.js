// ===========================================
// REGALBOX
// home.js
// ===========================================

document.addEventListener("DOMContentLoaded", () => {

    initHome();

});



function initHome() {

    initGatewaySpotlight();

}


// ===========================================
// GATEWAY PANEL — spotlight que sigue el mouse
// ===========================================

function initGatewaySpotlight() {

    const panel = document.getElementById("gatewayPanel");
    const spotlight = document.getElementById("gatewaySpotlight");

    if (!panel || !spotlight) return;

    panel.addEventListener("mousemove", (e) => {

        const rect = panel.getBoundingClientRect();

        spotlight.style.setProperty("--mx", `${e.clientX - rect.left}px`);
        spotlight.style.setProperty("--my", `${e.clientY - rect.top}px`);

    });

}

// ===========================================
// ADD TO CART AJAX
// ===========================================

function initAddToCart() {

    const form = document.getElementById("addToCartForm");

    if (!form) return;

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        try {

            const formData = new FormData(form);

            const response = await fetch(form.action, {

                method: "POST",

                body: formData,

                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }

            });

            const data = await response.json();

            if (!data.success) return;

            // =====================================
            // CONTADOR NAVBAR
            // =====================================

            document.querySelectorAll(".cart-count").forEach(counter => {

                counter.textContent = data.count;

            });


            // =====================================
            // TOTAL
            // =====================================

            const total = document.getElementById("cartTotal");

            if (total) {

                total.textContent = "$" + data.total;

            }


            // =====================================
            // ITEMS
            // =====================================

            const cartItems = document.getElementById("cartItems");

            if (cartItems) {

                cartItems.innerHTML = "";

                data.items.forEach(item => {

                    cartItems.innerHTML += `

                        <div class="flex gap-5 border-b border-[#ECE8E3] py-6">

                            <img
                                src="${item.image}"
                                class="h-24 w-24 rounded-2xl object-cover">

                            <div class="flex flex-1 flex-col">

                                <h3 class="font-semibold text-lg">

                                    ${item.name}

                                </h3>

                                <p class="mt-2 text-zinc-500">

                                    $${item.price}

                                </p>

                                <span class="mt-3 text-sm text-zinc-500">

                                    Cantidad: ${item.quantity}

                                </span>

                            </div>

                        </div>

                    `;

                });

            }


            // =====================================
            // ABRIR DRAWER
            // =====================================

            const overlay = document.getElementById("cartOverlay");
            const drawer = document.getElementById("cartDrawer");

            if (overlay && drawer) {

                overlay.classList.remove("hidden");
                overlay.classList.remove("opacity-0");

                drawer.classList.remove("translate-x-full");

                document.body.classList.add("overflow-hidden");

            }

        }

        catch (error) {

            console.error("Error al agregar al carrito:", error);

        }

    });

}