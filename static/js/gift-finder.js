// ===========================================
// REGALBOX
// GIFT FINDER (IA) — "Regi"
// ===========================================
//
// Se inyecta a sí mismo en el DOM (así no hace falta duplicar el
// markup del modal en cada template). Se abre desde cualquier botón
// con el atributo data-gift-finder-trigger.
//
// Reutiliza getCSRFToken()/getCookie() de cart2.js (se carga antes
// en todas las páginas) y loadCart()/openCart() para reflejar el
// carrito cuando se agrega una Box recomendada.

document.addEventListener("DOMContentLoaded", () => {
    initGiftFinder();
});

let gfOverlay, gfModal, gfPanel, gfMessages, gfInput, gfSendBtn, gfForm;
let gfWelcomeShown = false;
let gfWaiting = false;

const GF_WELCOME = "¡Hola! Soy Regi 🎁 Contame para quién es el regalo, para qué ocasión es y si tenés un presupuesto en mente, y te ayudo a encontrar la Box perfecta.";

function initGiftFinder() {

    injectGiftFinderMarkup();

    gfOverlay = document.getElementById("giftFinderOverlay");
    gfModal = document.getElementById("giftFinderModal");
    gfPanel = document.getElementById("giftFinderPanel");
    gfMessages = document.getElementById("giftFinderMessages");
    gfInput = document.getElementById("giftFinderInput");
    gfSendBtn = document.getElementById("giftFinderSend");
    gfForm = document.getElementById("giftFinderForm");

    document
        .querySelectorAll("[data-gift-finder-trigger]")
        .forEach(btn => btn.addEventListener("click", (e) => {
            e.preventDefault();
            openGiftFinder();
        }));

    document
        .getElementById("giftFinderClose")
        .addEventListener("click", closeGiftFinder);

    gfOverlay.addEventListener("click", closeGiftFinder);

    document
        .getElementById("giftFinderReset")
        .addEventListener("click", resetGiftFinder);

    gfForm.addEventListener("submit", (e) => {
        e.preventDefault();
        sendGiftFinderMessage();
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeGiftFinder();
    });

}

function injectGiftFinderMarkup() {

    const wrapper = document.createElement("div");

    wrapper.innerHTML = `
        <div id="giftFinderOverlay" class="fixed inset-0 z-[200] hidden bg-black/40 opacity-0 backdrop-blur-sm transition-all duration-500"></div>

        <div id="giftFinderModal" class="fixed inset-x-0 bottom-0 z-[210] hidden justify-center lg:inset-0 lg:items-center">

            <div
                id="giftFinderPanel"
                class="flex h-[82vh] max-h-[640px] w-full max-w-lg translate-y-full flex-col rounded-t-[32px] border border-[#F3B8C8] bg-[#FFFDFE] shadow-2xl transition-all duration-500 lg:translate-y-6 lg:rounded-[32px] lg:opacity-0">

                <div class="flex items-center justify-between border-b border-[#F3B8C8] px-6 py-5">

                    <div class="flex items-center gap-3">

                        <div class="flex h-11 w-11 items-center justify-center rounded-full bg-[#C60018] text-lg">
                            🎁
                        </div>

                        <div>
                            <p class="font-display text-2xl leading-none text-[#C60018]">Regi</p>
                            <p class="mt-1 text-xs text-[#9E3949]">Tu asistente de regalos</p>
                        </div>

                    </div>

                    <div class="flex items-center gap-2">

                        <button
                            type="button"
                            id="giftFinderReset"
                            class="rounded-full border border-[#F3B8C8] bg-white px-3 py-1.5 text-xs font-medium text-[#9E3949] transition hover:border-[#C60018] hover:text-[#C60018]">
                            Reiniciar
                        </button>

                        <button
                            type="button"
                            id="giftFinderClose"
                            class="flex h-9 w-9 items-center justify-center rounded-full border border-[#F3B8C8] bg-white text-[#C60018] transition hover:rotate-90 hover:bg-[#C60018] hover:text-white">
                            ✕
                        </button>

                    </div>

                </div>

                <div id="giftFinderMessages" class="flex-1 space-y-4 overflow-y-auto px-6 py-6"></div>

                <form id="giftFinderForm" class="flex items-center gap-3 border-t border-[#F3B8C8] px-5 py-4">

                    <input
                        id="giftFinderInput"
                        type="text"
                        maxlength="300"
                        autocomplete="off"
                        placeholder="Escribile a Regi..."
                        class="flex-1 rounded-full border border-[#F3B8C8] bg-[#FCE4EC] px-5 py-3 text-base outline-none transition focus:border-[#C60018]" style="font-size:16px;">

                    <button
                        id="giftFinderSend"
                        type="submit"
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#C60018] text-white transition hover:bg-[#9E0013] disabled:opacity-50">

                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/>
                        </svg>

                    </button>

                </form>

            </div>

        </div>
    `;

    document.body.appendChild(wrapper);

}

function openGiftFinder() {

    gfOverlay.classList.remove("hidden");
    gfModal.classList.remove("hidden");
    gfModal.classList.add("flex");

    requestAnimationFrame(() => {
        gfOverlay.classList.remove("opacity-0");
        gfPanel.classList.remove("translate-y-full", "lg:translate-y-6", "lg:opacity-0");
    });

    document.body.classList.add("overflow-hidden");

    if (!gfWelcomeShown) {
        appendBubble("assistant", GF_WELCOME);
        gfWelcomeShown = true;
    }

    gfInput.focus();

}

function closeGiftFinder() {

    gfOverlay.classList.add("opacity-0");
    gfPanel.classList.add("translate-y-full");

    setTimeout(() => {
        gfOverlay.classList.add("hidden");
        gfModal.classList.add("hidden");
        gfModal.classList.remove("flex");
    }, 400);

    document.body.classList.remove("overflow-hidden");

}

function resetGiftFinder() {

    const csrf = typeof getCSRFToken === "function" ? getCSRFToken() : "";

    fetch("/gift-finder/reset/", {
        method: "POST",
        headers: { "X-CSRFToken": csrf },
    }).finally(() => {
        gfMessages.innerHTML = "";
        gfWelcomeShown = false;
        appendBubble("assistant", GF_WELCOME);
        gfWelcomeShown = true;
    });

}

function appendBubble(role, text) {

    const bubble = document.createElement("div");

    if (role === "user") {

        bubble.className = "ml-auto max-w-[80%] rounded-[20px] rounded-br-md bg-[#C60018] px-5 py-3 text-sm text-white";
        bubble.textContent = text;

    } else {

        bubble.className = "max-w-[85%] rounded-[20px] rounded-bl-md bg-[#FCE4EC] px-5 py-3 text-sm text-[#7A0010]";
        bubble.textContent = text;

    }

    gfMessages.appendChild(bubble);
    gfMessages.scrollTop = gfMessages.scrollHeight;

    return bubble;

}

function appendTyping() {

    const bubble = document.createElement("div");

    bubble.id = "giftFinderTyping";
    bubble.className = "max-w-[60%] rounded-[20px] rounded-bl-md bg-[#FCE4EC] px-5 py-3 text-sm text-[#7A0010]";
    bubble.textContent = "Regi está escribiendo...";

    gfMessages.appendChild(bubble);
    gfMessages.scrollTop = gfMessages.scrollHeight;

}

function removeTyping() {

    const el = document.getElementById("giftFinderTyping");

    if (el) el.remove();

}

function appendBoxCard(box) {

    const card = document.createElement("div");

    card.className = "max-w-[85%] overflow-hidden rounded-[20px] border border-[#F3B8C8] bg-white";

    card.innerHTML = `
        <img src="${box.image}" alt="${box.name}" class="h-40 w-full object-cover">
        <div class="p-4">
            <p class="font-display text-2xl leading-none text-[#C60018]">${box.name}</p>
            <p class="mt-2 text-lg font-semibold">$${box.price}</p>
            <div class="mt-4 flex gap-2">
                <a href="${box.url}" class="flex-1 rounded-full border border-[#F3B8C8] px-4 py-2 text-center text-xs font-semibold text-[#C60018] transition hover:border-[#C60018]">
                    Ver esta Box
                </a>
                <button
                    type="button"
                    data-add-box="${box.id}"
                    class="flex-1 rounded-full bg-[#C60018] px-4 py-2 text-xs font-semibold text-white transition hover:bg-[#9E0013]">
                    Agregar al carrito
                </button>
            </div>
        </div>
    `;

    card.querySelector("[data-add-box]").addEventListener("click", async (e) => {

        const btn = e.currentTarget;
        btn.disabled = true;
        btn.textContent = "Agregando...";

        const csrf = typeof getCSRFToken === "function" ? getCSRFToken() : "";
        const fd = new FormData();
        fd.append("quantity", "1");

        const res = await fetch(`/cart/add/${box.id}/`, {
            method: "POST",
            body: fd,
            headers: { "X-CSRFToken": csrf, "X-Requested-With": "XMLHttpRequest" },
        });

        const data = await res.json();

        if (data.success) {

            btn.textContent = "¡Agregada! 🎉";

            document.querySelectorAll(".cart-count").forEach(el => {
                el.textContent = data.count;
            });

            if (typeof loadCart === "function") await loadCart();

        } else {

            btn.disabled = false;
            btn.textContent = data.error || "No se pudo agregar";

        }

    });

    gfMessages.appendChild(card);
    gfMessages.scrollTop = gfMessages.scrollHeight;

}

function appendWhatsappPrompt(url) {

    const wrap = document.createElement("a");

    wrap.href = url;
    wrap.target = "_blank";
    wrap.rel = "noopener noreferrer";
    wrap.className = "block max-w-[70%] rounded-full bg-[#C60018] px-5 py-3 text-center text-sm font-semibold text-white transition hover:bg-[#9E0013]";
    wrap.textContent = "Seguir por WhatsApp 💬";

    gfMessages.appendChild(wrap);
    gfMessages.scrollTop = gfMessages.scrollHeight;

}

async function sendGiftFinderMessage() {

    if (gfWaiting) return;

    const message = gfInput.value.trim();

    if (!message) return;

    appendBubble("user", message);
    gfInput.value = "";

    gfWaiting = true;
    gfSendBtn.disabled = true;
    gfInput.disabled = true;
    appendTyping();

    const csrf = typeof getCSRFToken === "function" ? getCSRFToken() : "";
    const fd = new FormData();
    fd.append("message", message);

    try {

        const res = await fetch("/gift-finder/chat/", {
            method: "POST",
            body: fd,
            headers: { "X-CSRFToken": csrf },
        });

        const data = await res.json();

        removeTyping();

        if (!data.success) {

            appendBubble("assistant", data.error || "No pude procesar tu mensaje, probá de nuevo.");

        } else {

            appendBubble("assistant", data.reply);

            if (data.recommended_box) {
                appendBoxCard(data.recommended_box);
            }

            if (data.limit_reached && data.whatsapp_url) {
                appendWhatsappPrompt(data.whatsapp_url);
            }

        }

    } catch (err) {

        removeTyping();
        appendBubble("assistant", "Ocurrió un error de conexión. Probá de nuevo en un momento.");

    } finally {

        gfWaiting = false;
        gfSendBtn.disabled = false;
        gfInput.disabled = false;
        gfInput.focus();

    }

}
