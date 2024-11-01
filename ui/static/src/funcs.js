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
            document.getElementById("toDraw").innerHTML =
                "ToDraw: " + data["toDraw"];
            document.getElementById("aicardcount").innerHTML =
                data["aicardcount"];
            document.getElementById("discardscroll").innerHTML =
                data["discardhistory"];
            document.getElementById("transcriptlist").innerHTML =
                data["movehistory"];
            // alert(data["movehistory"]);
            document.getElementById("futureimg1").innerHTML =
                '<img src="./static/imgs/' +
                data["card1"] +
                '.jpg" alt="Future1" /> <p class="futurelabel">Top</p>';
            document.getElementById("futureimg2").innerHTML =
                '<img src="./static/imgs/' +
                data["card2"] +
                '.jpg" alt="Future1" /> <p class="futurelabel">Top</p>';
            document.getElementById("futureimg3").innerHTML =
                '<img src="./static/imgs/' +
                data["card3"] +
                '.jpg" alt="Future1" /> <p class="futurelabel">Top</p>';
        })
        .catch((error) => console.error("Error:", error));
}
