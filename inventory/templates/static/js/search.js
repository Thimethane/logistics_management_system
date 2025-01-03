document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.querySelector("form");
    const searchInput = searchForm.querySelector("input[type='text']");
    searchInput.addEventListener("input", () => {
        if (searchInput.value.length < 3) {
            searchInput.setCustomValidity("Enter at least 3 characters to search.");
        } else {
            searchInput.setCustomValidity("");
        }
    });
});
