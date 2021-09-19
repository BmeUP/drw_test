from io import BytesIO
import os
import logging
import sqlite3
from pathlib import Path
from flask import Flask, flash, request, redirect, url_for, Response, g
from flask.helpers import send_file
from app.upload import allowed_file, generate_file_name, write_to_db
from app.delete import delete_folder, check_owner, delete_record
from app.decs import login_required
from app.download import get_file_name
from app.create_path import create_p


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(Path(__file__).parent) + "/store/"
app.config["SECRET_KEY"] = "the random string"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("database.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            hashed_filename = generate_file_name(file)
            file.seek(0)
            try:
                os.mkdir(create_p(app, hashed_filename, True))
                file.save(create_p(app, hashed_filename))
            except FileExistsError:
                return url_for("download_file", name=hashed_filename)
            write_to_db(get_db, file.filename, hashed_filename, request.authorization)
            return redirect(url_for("download_file", name=hashed_filename))
        return Response("sucses", status=200)


@app.route("/uploads/<string:name>", methods=["GET"])
def download_file(name):
    original_fn = get_file_name(get_db, name)
    if len(original_fn) > 0:
        with open(create_p(app, name), "rb") as f:
            buf = BytesIO(f.read())
            return send_file(buf, as_attachment=True, attachment_filename=original_fn[0][0])
    else:
        return Response("There is no spoon", status=404)


@app.route("/delete/<string:name>", methods=["DELETE"])
@login_required
def delete_file(name):
    try:
        files = len(os.listdir(create_p(app, name, True)))
    except FileNotFoundError:
        return Response("There is no spoon", status=404)

    if check_owner(get_db, name, request.authorization):
        delete_record(get_db, name, request.authorization)
        if files <= 1:
            delete_folder(create_p(app, name, True))
        else:
            os.remove(create_p(app, name))
        return Response("Deleted", status=200)
    else:
        return Response("You are not owner of this file", status=403)
