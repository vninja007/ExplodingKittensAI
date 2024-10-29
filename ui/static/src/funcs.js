function imageClicked(imageId) {
    fetch(`/image_clicked/${imageId}`)
        .then((response) => response.json())
        .then((data) => {
            document.getElementById("card0count").innerHTML = data.card0;
            document.getElementById("card1count").innerHTML = data.card1;
            document.getElementById("card2count").innerHTML = data.card2;
            document.getElementById("card3count").innerHTML = data.card3;
            document.getElementById("card4count").innerHTML = data.card4;
            document.getElementById("card5count").innerHTML = data.card5;
            document.getElementById("card6count").innerHTML = data.card6;
            document.getElementById("card7count").innerHTML = data.card7;
            document.getElementById("card8count").innerHTML = data.card8;
            document.getElementById("card9count").innerHTML = data.card9;
            document.getElementById("card10count").innerHTML = data.card10;
            document.getElementById("card11count").innerHTML = data.card11;
        })
        .catch((error) => console.error("Error:", error));
}
