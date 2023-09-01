from flask import Flask, render_template, request, make_response, abort
from os import listdir, getenv

import json

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

with open("static/data.json", "r") as f:
    PROJECTS_DATA = json.load(f)

PROJECTS = list(PROJECTS_DATA.keys())

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.route("/")
def home():
    return render_template("memories.html", project=PROJECTS_DATA.values())

@app.route("/<string:project>")
def project(project: str):

    if not project in PROJECTS:
        abort(404)

    # Get filenames
    images_fns = listdir(f"static/assets/{project}/thumbnails/img")
    images_fns.sort()

    film_thumb = listdir(f"static/assets/{project}/thumbnails/film")
    film_path = listdir(f"static/assets/{project}/film")
    film_thumb.sort()
    film_path.sort()

    films_fns = [(f,i) for f,i in zip(film_path, film_thumb)]

    return render_template("memorie-home.html", title=PROJECTS_DATA[project]["title"], headline=PROJECTS_DATA[project]["headline"], memory=project, subtitle=PROJECTS_DATA[project]["subtitle"], pictures=images_fns, films=films_fns, img_count=len(images_fns), film_count=len(films_fns))

@app.route("/<string:project>/viewer/<string:filetype>")
def viewer(project: str, filetype: str):    
    if not project in PROJECTS:
        abort(404)
    
    start = request.args.get("start", default=None)

    if start is None:
        abort(404)

    if filetype == "img":
        path = f"assets/{project}/img/{start}"
        return render_template("viewer-img.html", title=PROJECTS_DATA[project]["title"], memory=project, path=path, fn=start)
    elif filetype == "film":
        path = f"assets/{project}/film/{start}"
        return render_template("viewer-film.html", title=PROJECTS_DATA[project]["title"], memory=project, path=path, fn=start)
    else:
        abort(404)

@app.route("/<string:project>/all/<string:filetype>")
def seeall(project: str, filetype: str):
    if not project in PROJECTS:
        abort(404)

    if filetype != "img" and filetype != "film":
        abort(404)

    files = listdir(f"static/assets/{project}/{filetype}")
    files.sort()

    if filetype == "img":
        return render_template("seeall-img.html", title=PROJECTS_DATA[project]["title"], memory=project, file_count=len(files), filetype="Photos", links=[f"/static/assets/{project}/{filetype}/{name}" for name in files])
    elif filetype == "film":
        return render_template("seeall-film.html", title=PROJECTS_DATA[project]["title"], memory=project, file_count=len(files), filetype="Films", links=[f"/static/assets/{project}/{filetype}/{name}" for name in files])
    else:
        abort(404)

@app.route("/<string:project>/names/<string:filetype>")
def get_filenames(project: str, filetype: str):
    if not project in PROJECTS:
        abort(404)
    
    if filetype != "img" and filetype != "film":
        abort(404)
    
    files = listdir(f"static/assets/{project}/{filetype}")
    files.sort()

    # Offset index shift the names for next file to be in top of the list
    offset = request.args.get("offset", default="")

    try:
        offset_index = files.index(offset)
        files = files[offset_index::] + files[:offset_index:]
    except ValueError:
        pass

    return make_response({"filenames": files, "path": dict([(file, f"/static/assets/{project}/{filetype}/{file}") for file in files]), "descriptions": PROJECTS_DATA[project]["descriptions"]}, 200)

@app.route("/admin", methods=["GET", "POST"])
def connect_pannel():
    if request.method == "GET":
        return render_template("admin/connect.html")

    login, pswd = request.form.get("login", default=None), request.form.get("pswd", default=None)

    if login != getenv("ADMIN_LOGIN") or pswd != getenv("ADMIN_PSWD"):
        abort(403)

    return render_template("admin/pannel.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
