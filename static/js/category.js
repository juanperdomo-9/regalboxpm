// ===========================================
// REGALBOX
// CATEGORY — spotlight hover en las cards
// ===========================================
//
// El reveal-on-scroll y el smooth scroll ya los maneja animations.js
// (cargado en todas las páginas) — acá solo va el efecto de spotlight
// que sigue al mouse en .product-card (ver .product-card::before en
// el <style> de category.html).

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".product-card").forEach((card) => {

        card.addEventListener("mousemove", (e) => {

            const rect = card.getBoundingClientRect();

            card.style.setProperty("--mouse-x", `${e.clientX - rect.left}px`);
            card.style.setProperty("--mouse-y", `${e.clientY - rect.top}px`);

        });

    });

});
