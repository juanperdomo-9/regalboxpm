// ===========================================
// REGALBOX
// ANIMATIONS
// ===========================================

document.addEventListener("DOMContentLoaded", () => {

    revealElements();

    animateCards();

    buttonHover();

});


// ===========================================
// REVEAL
// ===========================================

function revealElements() {

    const targets = document.querySelectorAll(".reveal");

    // threshold 0: alcanza con que un solo pixel entre en pantalla.
    // Con un threshold más alto (ej. 0.15), bloques muy altos —como una
    // grilla de productos en una sola columna en mobile— nunca llegan a
    // cubrir ese % del viewport, y el bloque queda con opacidad 0 para
    // siempre (bug real detectado en "Box Dulces" en iPhone).
    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("revealed");
                observer.unobserve(entry.target);

            }

        });

    }, {

        threshold: 0

    });

    targets.forEach((el) => {

        observer.observe(el);

    });

    // Red de seguridad: si por lo que sea el observer no revela algo
    // (bug de navegador, elemento fuera de flujo, etc.), no se queda
    // invisible para siempre.
    setTimeout(() => {

        targets.forEach((el) => el.classList.add("revealed"));

    }, 2000);

}


// ===========================================
// STAGGER CARDS
// ===========================================

function animateCards() {

    document.querySelectorAll(".product-card").forEach((card, index) => {

        card.style.transitionDelay = `${index * 80}ms`;

    });

}


// ===========================================
// BUTTONS
// ===========================================

function buttonHover() {

    document.querySelectorAll("button, .btn").forEach(btn => {

        btn.addEventListener("mouseenter", () => {

            btn.style.transform = "translateY(-3px)";

        });

        btn.addEventListener("mouseleave", () => {

            btn.style.transform = "";

        });

    });

}