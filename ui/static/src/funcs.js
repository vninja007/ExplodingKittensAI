function imageClicked(imageId) {
    fetch(`/image_clicked/${imageId}`)
        .then((response) => response.text())
        // .then((data) => {
        //     alert(data); // Display the response from the server
        // })
        .catch((error) => console.error("Error:", error));
}
