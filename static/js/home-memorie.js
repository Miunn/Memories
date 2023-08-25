Array.from(document.getElementsByClassName("thumb_img")).forEach((img) => {
    img.addEventListener("click", (e) => {
        e.preventDefault();

        location.href += "/viewer/img?start="+img.id;
    })
});

Array.from(document.getElementsByClassName("thumb_film")).forEach((film) => {
    film.addEventListener("click", (e) => {
        e.preventDefault();

        location.href += "/viewer/film?start="+film.id;
    })
});