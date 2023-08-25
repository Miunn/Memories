const next = document.getElementById("next");
const prev = document.getElementById("prev");
const carrousel = document.getElementById("carrousel");

var currentIndex = 0;
var maxIndex = 0;

const loading = document.getElementById("loading");

function endLoad(parent, imgHTML) {
    //parent.appendChild(imgHTML);

    //loading.style.display = "none";
}

async function loadAll(HTMLParent, type) {
    const responseFiles = await fetch(`/elastique/names/${type}?offset=${carrousel.children[0].id}`);

    if (!responseFiles.ok) {
        return;
    }

    const data = await responseFiles.json();

    let i = data["filenames"].length;
    maxIndex = i;

    // First is load in template and has the data for offset
    for (file of data["filenames"].slice(1)) {
        if (type === "img") {
            loadImg(HTMLParent, file, data["path"][file], true, i*100);
        } else if (type === "film") {
            loadFilm(HTMLParent, file, data["path"][file], true, i*100);
        }

        i--;
    }
}

function loadImg(HTMLParent, filename, path, hide, zIndex) {
    let img = document.createElement("img");
    img.classList.add("img_viewer");
    img.classList.add("fadeOut");
    if (hide) {
        img.classList.add("hide");
    }
    img.id = filename;
    img.style.zIndex = zIndex;
    HTMLParent.appendChild(img);

    // Add load listener before fetching to be sure
    img.addEventListener("load", (e) => {
        endLoad(HTMLParent, e.target);
    });
            
    img.src = path;
}

function loadFilm(HTMLParent, filename, path, hide, zIndex) {
    let video = document.createElement("video");
    video.setAttribute("controls", "true");
    video.classList.add("img_viewer");
    if (hide) {
        video.classList.toggle("hide");
    }
    video.id = filename;
    video.style.zIndex = zIndex;
    HTMLParent.appendChild(video);

    // Add load listener before fetching to be sure
    video.addEventListener("load", (e) => {
        endLoad(HTMLParent, e.target);
    });
    video.src = path;
}

function goNext() {
    let imgs = carrousel.children;
    //imgs[currentIndex].classList.toggle("hide");
    imgs[currentIndex].classList.remove("fadeIn");
    imgs[currentIndex].classList.add("fadeOut");
    
    currentIndex = (currentIndex+1) % maxIndex;
    imgs[currentIndex].classList.remove("hide");
    imgs[currentIndex].classList.remove("fadeOut");
    imgs[currentIndex].classList.add("fadeIn");
}

function goPrev() {
    let imgs = carrousel.children;
    //imgs[currentIndex].classList.add("hide");
    imgs[currentIndex].classList.remove("fadeIn");
    imgs[currentIndex].classList.add("fadeOut");
    currentIndex = (currentIndex+maxIndex-1) % maxIndex;    // +maxIndex because in JS -1%x=-1 et non x-1 donc on ajoute x pour loop
    imgs[currentIndex].classList.remove("hide");
    imgs[currentIndex].classList.remove("fadeOut");
    imgs[currentIndex].classList.add("fadeIn");
}

next.addEventListener("click", (e) => {
    e.preventDefault();

    goNext();
});

prev.addEventListener("click", (e) => {
    e.preventDefault();

    goPrev();
});

document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
        goNext();
    } else if (e.key === "ArrowLeft") {
        goPrev();
    }
})