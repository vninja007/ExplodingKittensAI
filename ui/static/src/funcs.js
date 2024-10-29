function imageClicked(imageId) {
    fetch(`/image_clicked/${imageId}`)
        .then((response) => response.json())
        .then((data) => {
            for (let i = 0; i < 12; i++) {
                document.getElementById(`card${i}count`).innerHTML =
                    data[`card${i}`];

                if (i == 0 || i == 1 || data[`card${i}`] <= 0 + i / 7) {
                    el = document.getElementById(`card${i}img`);
                    el.classList.add("unplayable");
                    el.onclick = null;
                } else {
                    el = document.getElementById(`card${i}img`);
                    el.classList.remove("unplayable");
                    el.onclick = function () {
                        imageClicked(i);
                    };
                }
            }
            document.getElementById("turnis").innerHTML = [
                "Player: Human",
                "Player: AI",
            ][data["turn"]];
            document.getElementById("deckcount").innerHTML = data["decklen"];
            if (data["isOver"] === 0) {
                document.getElementById("deadindicator").innerHTML =
                    "Human win!";
            } else if (data["isOver"] === 1) {
                document.getElementById("deadindicator").innerHTML = "AI win!";
            } else {
                document.getElementById("deadindicator").innerHTML =
                    "Game Not Over";
            }
        })
        .catch((error) => console.error("Error:", error));
}
