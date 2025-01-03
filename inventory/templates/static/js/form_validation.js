document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    form.addEventListener("submit", (event) => {
        const requiredFields = form.querySelectorAll("[required]");
        let isValid = true;
        requiredFields.forEach((field) => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add("error");
            } else {
                field.classList.remove("error");
            }
        });
        if (!isValid) {
            event.preventDefault();
            alert("Please fill in all required fields.");
        }
    });
});
