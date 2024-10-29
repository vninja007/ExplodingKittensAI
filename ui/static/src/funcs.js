function imageClicked(imageId) {
    fetch(`/image_clicked/${imageId}`)
        .then((response) => response.json())
        .then((data) => {
            for (var i = 0; i < 12; i++) {
                document.getElementById(`card${i}count`).innerHTML =
                    data[`card${i}`];

                if (i == 0 || i == 1 || data[`card${i}`] <= 0 + i / 7) {
                    document
                        .getElementById(`card${i}img`)
                        .classList.add("unplayable");
                } else {
                    document
                        .getElementById(`card${i}img`)
                        .classList.remove("unplayable");
                }
            }
        })
        .catch((error) => console.error("Error:", error));
}

window.onload = function () {
    imageClicked(999);
};
