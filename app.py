from flask import Flask, render_template, request, make_response, abort, send_file
from os import listdir, getenv, path, walk
from shutil import rmtree

import json

from dotenv import load_dotenv

# For files downloading
from io import BytesIO
from zipfile import ZipFile

load_dotenv()


app = Flask(__name__)

with open("static/data.json", "r") as f:
    PROJECTS_DATA = json.load(f)

def project_exist(project):
    return project in PROJECTS_DATA

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.route("/")
def home():
    return render_template("memories.html", project=PROJECTS_DATA.values())

@app.route("/<string:project>")
def project(project: str):

    if not project_exist(project):
        abort(404)

    # Get filenames
    images_fns = listdir(f"static/assets/{project}/thumbnails/img")
    images_fns.sort()

    film_thumb = listdir(f"static/assets/{project}/thumbnails/film")
    film_path = listdir(f"static/assets/{project}/film")
    film_thumb.sort()
    film_path.sort()

    films_fns = [(f,i) for f,i in zip(film_path, film_thumb)]

    return render_template("memorie-home.html", title=PROJECTS_DATA[project]["title"], headline=PROJECTS_DATA[project]["headline"], memory=project, subtitle=PROJECTS_DATA[project]["subtitle"], pictures=images_fns, films=films_fns, img_count=PROJECTS_DATA[project]["photo_count"], film_count=PROJECTS_DATA[project]["film_count"])

@app.route("/<string:project>/viewer/<string:filetype>")
def viewer(project: str, filetype: str):    
    if not project_exist(project):
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
    if not project_exist(project):
        abort(404)

    if filetype != "img" and filetype != "film":
        abort(404)

    files = listdir(f"static/assets/{project}/{filetype}")
    files.sort()

    if filetype == "img":
        return render_template("seeall-img.html", title=PROJECTS_DATA[project]["title"], memory=project, file_count=PROJECTS_DATA[project]["photo_count"], filetype="Photos", links=[f"/static/assets/{project}/{filetype}/{name}" for name in files])
    elif filetype == "film":
        return render_template("seeall-film.html", title=PROJECTS_DATA[project]["title"], memory=project, file_count=PROJECTS_DATA[project]["film_count"], filetype="Films", links=[f"/static/assets/{project}/{filetype}/{name}" for name in files])
    else:
        abort(404)

@app.route("/<string:project>/names/<string:filetype>")
def get_filenames(project: str, filetype: str):
    if not project_exist(project):
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

    return render_template("admin/pannel.html", memories=PROJECTS_DATA)

@app.route("/admin/edit/<string:project>")
def edit_project(project: str):
    if not project_exist(project):
        abort(404)

    return render_template("edit-memory.html")

@app.route("/download/<string:project>")
def download_project(project: str):
    if not project_exist(project):
        abort(404)

    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for parent_path, folders, files in walk(f"static/assets/{project}"):
            for folder in folders:
                zf.write(path.join(parent_path, folder), path.join(parent_path, folder).replace(f"static/assets/{project}", ""))

            for file in files:
                zf.write(path.join(parent_path, file), path.join(parent_path, file).replace(f"static/assets/{project}", ""))
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name=f'{project}.zip'
    )

@app.route("/size/<string:project>")
def get_project_size(project: str):
    if not project_exist(project):
        abort(404)

    project_path = f"static/assets/{project}"
    img_path = f"static/assets/{project}/img"
    film_path = f"static/assets/{project}/film"
    thumbnails_path = f"static/assets/{project}/thumbnails"
    paths = [project_path, img_path, film_path, thumbnails_path]

    sizes = [0, 0, 0, 0]
    for i in range(len(paths)):
        for p, d, f in walk(paths[i]):
            sizes[i] += sum([path.getsize(path.join(p, file)) for file in f])

    return make_response({"memory": project, "size": sizes[0], "photo_size": sizes[1], "film_size": sizes[2], "thumbnails": sizes[3]})

@app.route("/admin/delete/<string:project>")
def delete_project(project: str):
    if not project_exist(project):
        abort(404)

    try:
        rmtree(f"static/assets/{project}")

        del PROJECTS_DATA[project]
        
        with open("static/data.json", "w") as f:
            f.write(json.dumps(PROJECTS_DATA))

        return make_response("No Content", 204)
    except Exception as e:
        return make_response({"error": str(e)}, 500)

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
