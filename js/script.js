/* =====================================================
   PRAGU SOFTWARE SOLUTIONS
   GLOBAL JAVASCRIPT
===================================================== */


/* =====================================================
   PAGE LOADER
===================================================== */

window.addEventListener("load", () => {

    const loader =
        document.querySelector(".page-loader");

    if (loader) {

        setTimeout(() => {

            loader.classList.add("loaded");

        }, 600);

    }

});

/* =====================================================
   THEME SYSTEM
===================================================== */

const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");

// Load saved theme
const savedTheme = localStorage.getItem("pragu-theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");

    if (themeIcon) {
        themeIcon.textContent = "☀";
    }
} else {
    document.body.classList.remove("dark-theme");

    if (themeIcon) {
        themeIcon.textContent = "☾";
    }
}

// Toggle theme
if (themeToggle) {

    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("dark-theme");

        const isDark =
            document.body.classList.contains("dark-theme");

        if (isDark) {

            themeIcon.textContent = "☀";

            localStorage.setItem(
                "pragu-theme",
                "dark"
            );

        } else {

            themeIcon.textContent = "☾";

            localStorage.setItem(
                "pragu-theme",
                "light"
            );

        }

    });

}


/* =====================================================
   MOBILE NAVIGATION
===================================================== */

const menuBtn =
    document.getElementById("menuBtn");

const navLinks =
    document.querySelector(".nav-links");


if (menuBtn) {

    menuBtn.addEventListener(
        "click",
        () => {

            navLinks.classList.toggle(
                "show"
            );

        }
    );

}


/* Close menu */

document
    .querySelectorAll(".nav-links a")
    .forEach(link => {

        link.addEventListener(
            "click",
            () => {

                navLinks.classList.remove(
                    "show"
                );

            }
        );

    });


/* =====================================================
   SCROLL REVEAL
===================================================== */

const revealElements =
    document.querySelectorAll(".reveal");


const revealObserver =
    new IntersectionObserver(
        entries => {

            entries.forEach(
                entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "show"
                        );

                        revealObserver.unobserve(
                            entry.target
                        );

                    }

                }
            );

        },

        {
            threshold: 0.12
        }

    );


revealElements.forEach(
    element => {

        revealObserver.observe(
            element
        );

    }
);


/* =====================================================
   PAGE TRANSITION
===================================================== */

document
    .querySelectorAll(
        'a[href$=".html"]'
    )
    .forEach(link => {

        link.addEventListener(
            "click",
            event => {

                const href =
                    link.getAttribute("href");


                /* Ignore same page */

                if (
                    href ===
                    window.location.pathname
                    .split("/")
                    .pop()
                ) {

                    return;

                }


                event.preventDefault();


                document.body.classList.add(
                    "page-exit"
                );


                setTimeout(
                    () => {

                        window.location.href =
                            href;

                    },

                    350
                );

            }
        );

    });


/* =====================================================
   CARD MOUSE EFFECT
===================================================== */

const cards =
    document.querySelectorAll(
        ".service-card, .why-card"
    );


cards.forEach(card => {

    card.addEventListener(
        "mousemove",
        event => {

            const rect =
                card.getBoundingClientRect();


            const x =
                event.clientX -
                rect.left;


            const y =
                event.clientY -
                rect.top;


            const centerX =
                rect.width / 2;


            const centerY =
                rect.height / 2;


            const rotateX =
                (y - centerY) / 18;


            const rotateY =
                (centerX - x) / 18;


            card.style.transform =
                `perspective(700px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-8px)`;

        }
    );


    card.addEventListener(
        "mouseleave",
        () => {

            card.style.transform =
                "";

        }
    );

});


/* =====================================================
   NAVBAR SCROLL EFFECT
===================================================== */

const navbar =
    document.querySelector(".navbar");


window.addEventListener(
    "scroll",
    () => {

        if (
            window.scrollY > 30
        ) {

            navbar.classList.add(
                "scrolled"
            );

        }

        else {

            navbar.classList.remove(
                "scrolled"
            );

        }

    }
);


/* =====================================================
   BUTTON RIPPLE
===================================================== */

document
    .querySelectorAll(
        ".primary-btn, .secondary-btn, .outline-btn"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            function(event) {

                const ripple =
                    document.createElement(
                        "span"
                    );


                ripple.classList.add(
                    "ripple"
                );


                this.appendChild(
                    ripple
                );


                setTimeout(
                    () => {

                        ripple.remove();

                    },

                    600
                );

            }
        );

    });