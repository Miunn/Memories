from flask import Flask, render_template, request, make_response
from os import listdir, path

import json

app = Flask(__name__)

with open("static/data.json", "r") as f:
    PROJECTS_DATA = json.load(f)

PROJECTS = list(PROJECTS_DATA.keys())

@app.route("/")
def home():
    return render_template("memories.html", project=PROJECTS_DATA.values())

@app.route("/<string:project>")
def project(project: str):

    if not project in PROJECTS:
        return make_response("Not found", 404)

    # Get filenames
    images_fns = listdir("static/assets/elastique/thumbnails/img")
    images_fns.sort()

    film_thumb = listdir("static/assets/elastique/thumbnails/film")
    film_path = listdir("static/assets/elastique/film")
    film_thumb.sort()
    film_path.sort()

    films_fns = [(f,i) for f,i in zip(film_path, film_thumb)]

    return render_template("memorie-home.html", headline=PROJECTS_DATA[project]["headline"], subtitle=PROJECTS_DATA[project]["subtitle"], pictures=images_fns, films=films_fns, img_count=len(images_fns), film_count=len(films_fns))

@app.route("/<string:project>/viewer/<string:filetype>")
def viewer(project: str, filetype: str):    
    if not project in PROJECTS:
        return make_response("Not Found", 404)
    
    start = request.args.get("start", default=None)

    if start is None:
        return make_response("Not Found", 404)

    if filetype == "img":
        path = f"assets/{project}/img/{start}"
        return render_template("viewer-img.html", memorie=project, path=path, fn=start)
    elif filetype == "film":
        path = f"assets/{project}/film/{start}"
        return render_template("viewer-film.html", memorie=project, path=path, fn=start)
    else:
        return make_response("UNKNOWN TYPE", 400)

@app.route("/<string:project>/names/<string:filetype>")
def get_filenames(project: str, filetype: str):
    if not project in PROJECTS:
        return make_response("Not Found", 404)
    
    if filetype != "img" and filetype != "film":
        return make_response("Not Found", 404)
    
    files = listdir(f"static/assets/{project}/{filetype}")
    files.sort()

    # Offset index shift the names for next file to be in top of the list
    offset = request.args.get("offset", default="")

    try:
        offset_index = files.index(offset)
        files = files[offset_index::] + files[:offset_index:]
    except ValueError:
        pass

    #return make_response({"filenames": files, "path": dict([(file, f"/static/assets/{project}/{filetype}/{file}") for file in files])}, 200)   # Like this dict() unsort the list
    return make_response({"filenames": files, "path": dict([(file, f"/static/assets/{project}/{filetype}/{file}") for file in files])}, 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
