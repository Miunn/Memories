Array.from(document.getElementsByClassName("list-img")).forEach((elmt) => {
    elmt.addEventListener("click", (event) => {
        window.open(event.target.src, 'Image');
    });
});