const currentCounter = document.getElementById("current");
const maxCounter = document.getElementById("total");
const next = document.getElementById("next");
const prev = document.getElementById("prev");
const carrousel = document.getElementById("carrousel");

var currentIndex = 0;
var maxIndex = 0;

const loading = document.getElementById("loading");

function endLoad(imgHTML) {
    imgHTML.parentNode.style.width = imgHTML.width + "px";
    imgHTML.parentNode.style.height = imgHTML.height + "px";
}

async function loadAll(HTMLParent, type) {
    const params = new URLSearchParams(window.location.search)
    const responseFiles = await fetch(`/elastique/names/${type}?offset=${params.get("start")}`);

    if (!responseFiles.ok) {
        return;
    }

    const data = await responseFiles.json();

    let i = data["filenames"].length;
    maxIndex = i;
    maxCounter.innerText = maxIndex;

    if (type === "img") {
        let firstFile = data["filenames"][0];
        loadImg(HTMLParent, firstFile, data["path"][firstFile], false, i*100, data["descriptions"][firstFile]);
        console.log("load false");
        i--;
    }


    // First is load in template and has the data for offset
    for (file of data["filenames"].slice(1)) {
        if (type === "img") {
            loadImg(HTMLParent, file, data["path"][file], true, i*100, data["descriptions"][file]);
        } else if (type === "film") {
            loadFilm(HTMLParent, file, data["path"][file], true, i*100, data["descriptions"][file]);
        }

        i--;
    }
}

function loadImg(HTMLParent, filename, path, hide, zIndex, HTMLdescription) {
    console.log("load:"+hide);
    let wrapperDiv = document.createElement("div");
    wrapperDiv.classList.add("img-wrapper");
    let img = document.createElement("img");
    img.classList.add("img_viewer");
    wrapperDiv.classList.add("hide");

    img.id = filename;

    wrapperDiv.style.zIndex = zIndex+10;
    img.style.zIndex = zIndex;

    wrapperDiv.appendChild(img);
    HTMLParent.appendChild(wrapperDiv);

    // Add load listener before fetching to be sure
    if (hide) {
        img.addEventListener("load", (e) => {
            endLoad(e.target);
        });
    } else {
        img.addEventListener("load", (e) => {
            endLoad(e.target);
            e.target.parentNode.classList.remove("hide");
            e.target.parentNode.classList.remove("fadeOut");
            e.target.parentNode.classList.add("fadeIn");
        });
    }
       
    img.src = path;

    let description = document.createElement("p");
    description.classList.add("img-description");
    description.style.zIndex = zIndex+1;
    description.innerHTML = HTMLdescription;

    wrapperDiv.appendChild(description);
}

function loadFilm(HTMLParent, filename, path, hide, zIndex) {
    let video = document.createElement("video");
    video.setAttribute("controls", "true");
    video.classList.add("img_viewer");
    if (hide) {
        video.classList.add("hide");
    }
    video.id = filename;
    video.style.zIndex = zIndex;
    HTMLParent.appendChild(video);

    // Add load listener before fetching to be sure
    video.addEventListener("load", (e) => {
        endLoad(e.target);
    });
    video.src = path;
}

function goNext() {
    let imgsWrapper = carrousel.children;
    imgsWrapper[currentIndex].classList.remove("fadeIn");
    imgsWrapper[currentIndex].classList.add("fadeOut");
    
    currentIndex = (currentIndex+1) % maxIndex;
    currentCounter.innerText = currentIndex+1;

    imgsWrapper[currentIndex].classList.remove("hide");
    imgsWrapper[currentIndex].classList.remove("fadeOut");
    imgsWrapper[currentIndex].classList.add("fadeIn");
}

function goPrev() {
    let imgsWrapper = carrousel.children;
    imgsWrapper[currentIndex].classList.remove("fadeIn");
    imgsWrapper[currentIndex].classList.add("fadeOut");

    currentIndex = (currentIndex+maxIndex-1) % maxIndex;    // +maxIndex because in JS -1%x=-1 et non x-1 donc on ajoute x pour loop
    currentCounter.innerText = currentIndex+1;
    
    imgsWrapper[currentIndex].classList.remove("hide");
    imgsWrapper[currentIndex].classList.remove("fadeOut");
    imgsWrapper[currentIndex].classList.add("fadeIn");
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
});
