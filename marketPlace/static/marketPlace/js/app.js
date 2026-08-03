// =========================
// Mobile Navigation
// =========================

const menuBtn = document.getElementById("menuBtn");
const navMenu = document.getElementById("navMenu");

if (menuBtn && navMenu) {

    menuBtn.addEventListener("click", () => {

        navMenu.classList.toggle("active");

    });

}



// =========================
// Auto Hide Django Messages
// =========================

function dismissAlert(alert) {

    alert.style.transition = "0.4s";

    alert.style.opacity = "0";

    alert.style.transform = "translateY(-10px)";

    setTimeout(() => {

        alert.remove();

    }, 400);

}

const alerts = document.querySelectorAll(".alert");

alerts.forEach(alert => {

    const timer = setTimeout(() => {

        dismissAlert(alert);

    }, 3500);

    const closeBtn = alert.querySelector(".alert-close");

    if (closeBtn) {

        closeBtn.addEventListener("click", () => {

            clearTimeout(timer);

            dismissAlert(alert);

        });

    }

});



// =========================
// Account Dropdown
// =========================

const accountMenu = document.getElementById("accountMenu");
const accountTrigger = document.getElementById("accountTrigger");

if (accountMenu && accountTrigger) {

    accountTrigger.addEventListener("click", (event) => {

        event.stopPropagation();

        accountMenu.classList.toggle("active");

    });

    document.addEventListener("click", (event) => {

        if (!accountMenu.contains(event.target)) {

            accountMenu.classList.remove("active");

        }

    });

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {

            accountMenu.classList.remove("active");

        }

    });

}



// =========================
// Confirm Delete (custom modal)
// =========================

const confirmModal = document.createElement("div");

confirmModal.className = "confirm-modal";

confirmModal.innerHTML = `
    <div class="confirm-modal-box">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <h3>Remove this item?</h3>
        <p>This product will be removed from your cart.</p>
        <div class="confirm-modal-actions">
            <button type="button" class="btn btn-secondary" data-action="cancel">Cancel</button>
            <a href="#" class="btn btn-danger" data-action="confirm">Remove</a>
        </div>
    </div>
`;

document.body.appendChild(confirmModal);

const confirmLink = confirmModal.querySelector("[data-action='confirm']");
const cancelBtn = confirmModal.querySelector("[data-action='cancel']");

function closeConfirmModal() {
    confirmModal.classList.remove("active");
}

document.querySelectorAll(".remove-btn").forEach(button => {

    button.addEventListener("click", function (event) {

        event.preventDefault();

        confirmLink.setAttribute("href", button.getAttribute("href"));

        confirmModal.classList.add("active");

    });

});

cancelBtn.addEventListener("click", closeConfirmModal);

confirmModal.addEventListener("click", (event) => {

    if (event.target === confirmModal) {
        closeConfirmModal();
    }

});

document.addEventListener("keydown", (event) => {

    if (event.key === "Escape") {
        closeConfirmModal();
    }

});



// =========================
// Button Loading Effect
// =========================

const forms = document.querySelectorAll("form");

forms.forEach(form => {

    form.addEventListener("submit", () => {

        const submitButton = form.querySelector(
            "button[type='submit']"
        );

        if (submitButton) {

            submitButton.disabled = true;

            submitButton.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';

        }

    });

});



// =========================
// Card Hover Animation
// =========================

const cards = document.querySelectorAll(".product-card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transition = ".3s";

    });

});



// =========================
// Smooth Scroll
// =========================

document.querySelectorAll("a[href^='#']").forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(
            this.getAttribute("href")
        );

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});



// =========================
// Image Preview
// (Future Admin Feature)
// =========================

const imageInput = document.getElementById("imageInput");

const imagePreview = document.getElementById("imagePreview");

if (imageInput && imagePreview) {

    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {

            imagePreview.src = e.target.result;

        }

        reader.readAsDataURL(file);

    });

}



// =========================
// Quantity Stepper (product detail)
// =========================

document.querySelectorAll(".quantity-selector").forEach(selector => {

    const input = selector.querySelector("input[type='number']");

    selector.querySelectorAll("[data-step]").forEach(button => {

        button.addEventListener("click", () => {

            if (!input) return;

            const step = parseInt(button.dataset.step, 10);
            const min = parseInt(input.min || "1", 10);
            const max = parseInt(input.max || "9999", 10);
            const current = parseInt(input.value || "1", 10);

            input.value = Math.min(max, Math.max(min, current + step));

        });

    });

});



// =========================
// Quantity Animation
// =========================

const quantityButtons = document.querySelectorAll(".quantity-btn");

quantityButtons.forEach(button => {

    button.addEventListener("click", () => {

        button.animate(

            [

                { transform: "scale(1)" },

                { transform: "scale(.85)" },

                { transform: "scale(1)" }

            ],

            {

                duration: 180

            }

        );

    });

});



// =========================
// Scroll To Top Button
// =========================

const scrollButton = document.createElement("button");

scrollButton.innerHTML =
'<i class="fa-solid fa-arrow-up"></i>';

scrollButton.className = "scroll-top";

document.body.appendChild(scrollButton);

scrollButton.style.position = "fixed";
scrollButton.style.bottom = "25px";
scrollButton.style.right = "25px";
scrollButton.style.width = "48px";
scrollButton.style.height = "48px";
scrollButton.style.borderRadius = "50%";
scrollButton.style.display = "none";
scrollButton.style.border = "none";
scrollButton.style.cursor = "pointer";
scrollButton.style.background = "#2563eb";
scrollButton.style.color = "#fff";
scrollButton.style.boxShadow = "0 10px 25px rgba(0,0,0,.15)";
scrollButton.style.zIndex = "999";

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        scrollButton.style.display = "block";

    }

    else {

        scrollButton.style.display = "none";

    }

});

scrollButton.addEventListener("click", () => {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

});



// =========================
// Console
// =========================

console.log("AlphaShop Ready");