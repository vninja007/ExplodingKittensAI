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
                data["deck"][data["deck"].length - 1] +
                '.jpg" alt="Future1" /> <p class="futurelabel">Top</p>';
            if (data["deck"].length >= 2) {
                document.getElementById("futureimg2").innerHTML =
                    '<img src="./static/imgs/' +
                    data["deck"][data["deck"].length - 2] +
                    '.jpg" alt="Future1" /> <p class="futurelabel">2nd</p>';
            } else {
                document.getElementById("futureimg2").innerHTML = "";
            }
            if (data["deck"].length >= 3) {
                document.getElementById("futureimg3").innerHTML =
                    '<img src="./static/imgs/' +
                    data["deck"][data["deck"].length - 3] +
                    '.jpg" alt="Future1" /> <p class="futurelabel">3rd</p>';
            } else {
                document.getElementById("futureimg3").innerHTML = "";
            }

            if (data["cardplayed"] == 6) {
                document.getElementById("futuresee").classList.remove("unseen");
            } else {
                document.getElementById("futuresee").classList.add("unseen");
            }
        })
        .catch((error) => console.error("Error:", error));
}
