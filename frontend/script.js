const imageInput = document.getElementById("imageInput");

const preview = document.getElementById("preview");

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (file) {

        preview.src = URL.createObjectURL(file);

        preview.style.display = "block";
    }
});

async function detectImage() {

    const file = imageInput.files[0];

    if (!file) {

        alert("Please upload image first");

        return;
    }

    document.getElementById("result").innerText =
    "Analyzing...";

    const formData = new FormData();

    formData.append("image", file);

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/detect",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        console.log(data);

        document.getElementById("result").innerText =
        data.label;

        document.getElementById("probability").innerText =
        data.confidence + "%";

    } catch (error) {

        console.log(error);

        document.getElementById("result").innerText =
        "Error detecting image";
    }
}