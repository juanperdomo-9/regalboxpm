// ===========================================
// REGALBOX
// navbar.js
// ===========================================

document.addEventListener("DOMContentLoaded", () => {

    initNavbar();

    initMobileMenu();

    initSmoothScroll();

});



// ===========================================
// NAVBAR SCROLL
// ===========================================

function initNavbar() {

    const navbar = document.getElementById("navbar");

    const container = document.getElementById("navbarContainer");

    if (!navbar || !container) return;

    window.addEventListener("scroll", () => {

        if (window.scrollY > 30) {

            container.classList.add(
                "shadow-xl",
                "bg-white/90",
                "backdrop-blur-3xl"
            );

            container.classList.remove(
                "bg-white/60"
            );

        }

        else {

            container.classList.remove(
                "shadow-xl",
                "bg-white/90"
            );

            container.classList.add(
                "bg-white/60"
            );

        }

    });

}



// ===========================================
// MOBILE MENU
// ===========================================

function initMobileMenu() {

    const button = document.getElementById("mobileMenuButton");

    const menu = document.getElementById("mobileMenu");

    const content = document.getElementById("mobileMenuContent");

    if (!button || !menu || !content) return;

    button.addEventListener("click", () => {

        menu.classList.remove("hidden");

        document.body.classList.add("overflow-hidden");

    });

    menu.addEventListener("click", (e) => {

        if (e.target === menu) {

            closeMenu();

        }

    });

    document.querySelectorAll("#mobileMenu a").forEach((link) => {

        link.addEventListener("click", () => {

            closeMenu();

        });

    });

    document.addEventListener("keydown", (e) => {

        if (e.key === "Escape") {

            closeMenu();

        }

    });

    function closeMenu() {

        menu.classList.add("hidden");

        document.body.classList.remove("overflow-hidden");

    }

}



// ===========================================
// SMOOTH SCROLL
// ===========================================

function initSmoothScroll() {

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(

                this.getAttribute("href")

            );

            if (!target) return;

            e.preventDefault();

            target.scrollIntoView({

                behavior: "smooth",

                block: "start"

            });

        });

    });

}