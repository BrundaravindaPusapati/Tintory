document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('input[type="file"]');
    const form = document.querySelector("form");

    // Create preview image
    const preview = document.createElement("img");
    preview.style.maxWidth = "300px";
    preview.style.display = "none";
    preview.style.marginTop = "10px";

    form.appendChild(preview);

    // Create loading text
    const loadingText = document.createElement("p");
    loadingText.innerText = "Processing image... please wait ⏳";
    loadingText.style.display = "none";
    form.appendChild(loadingText);

    // Show preview when image selected
    fileInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            // Validate file type
            if (!file.type.startsWith("image/")) {
                alert("Please upload a valid image file!");
                fileInput.value = "";
                preview.style.display = "none";
                return;
            }

            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };

            reader.readAsDataURL(file);
        }
    });

    // Show loading when form is submitted
    form.addEventListener("submit", function () {
        loadingText.style.display = "block";
    });
});
