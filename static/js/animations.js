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

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("revealed");

            }

        });

    }, {

        threshold: 0.15

    });

    document.querySelectorAll(".reveal").forEach((el) => {

        observer.observe(el);

    });

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