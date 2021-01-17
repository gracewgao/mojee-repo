from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    jsonify,
    g,
    abort,
    send_from_directory,
)
from werkzeug.exceptions import abort
from .db import get_db

import time
import os
from hashlib import md5
from PIL import Image

from werkzeug.utils import secure_filename

from .vision import *

bp = Blueprint("images", __name__)


def check_extension(extension):
    return extension in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route("/gallery")
def gallery():

    db = get_db()
    images = db.execute(
        "SELECT image_id, detail FROM images ORDER BY created_on desc"
    ).fetchall()

    if not images:
        abort(404, "No images found.")
    else:
        images_json = []
        for i in images:
            images_json.append({"image_id": i[0], "detail": i[1]})

    return jsonify(images_json)


def add_pic(filename):
    labels = vision_label(filename)

    g.db.execute(
        "INSERT INTO images (filename) VALUES (?) RETURNING image_id", [filename]
    )
    image_id = g.db.execute("SELECT last_insert_rowid()")

    for label, score in labels.items():
        g.db.execute(
            "INSERT INTO keywords_images (image_id, keyword, score) VALUES (?, ?, ?)",
            (image_id, label, score),
        )

    g.db.commit()


@bp.route("/gallery/add", methods={"POST"})
def add_image():
    image_file = request.files["file"]
    detail = json.loads(request.args.data("data", ""))

    try:
        extension = image_file.filename.rsplit(".", 1)[1].lower()
    except IndexError as err:
        current_app.logger.info(err)
        abort(404)
    if image_file and check_extension(extension):
        # salt and hash the file contents
        filename = (
            md5(image_file.read()).hexdigest()
            + str(round(time.time() * 1000))
            + "."
            + extension
        )
        image_file.seek(0)
        image_file.save(os.path.join(current_app.config["UPLOAD_DIR"], filename))
        add_pic(filename)
        return redirect(url_for("show_pic", filename=filename))
    else:
        abort(404)


@bp.route("/gallery/search", methods={"GET"})
def search():

    db = get_db()
    images = db.execute("SELECT image_id, filename, detail FROM images").fetchall()

    json = request.get_json(force=True)
    emoji = json["emoji"]

    images_json = []

    # attempts to match keywords of image with emoji
    for i in images:
        filename = i[1]
        image_keywords = db.execute(
            "SELECT keyword, score FROM keywords_images WHERE image_id = (?)", i[0]
        ).fetchall()

        labels = {}
        for k in image_keywords:
            word = k[0]
            score = k[1]
            if not labels[word]:
                labels[word] = score
            else:
                labels[word] = max(labels[word], score)

        match = vision_match(labels, emoji)
        if match:
            images_json.append({"image_id": i[0], "filename": i[1], "detail": i[2]})

    return jsonify(images_json)


@bp.route("/mojees/add", methods=["POST"])
def add_mojee():
    db = get_db()

    json = request.get_json(force=True)
    emoji = json["emoji"]
    keyword = json["keyword"]

    db.execute("INSERT INTO mojees" " VALUES (?, ?)", (emoji, keyword))
    db.commit()

    return jsonify({"status": "success"})


@bp.route("/mojees/delete", methods=["POST"])
def delete_mojee():
    db = get_db()

    json = request.get_json(force=True)
    emoji = json["emoji"]
    keyword = json["keyword"]

    db.execute(
        "DELETE from mojees WHERE" " emoji == (?) AND keyword == (?)", (emoji, keyword)
    )
    db.commit()

    return jsonify({"status": "success"})


@bp.route("/mojees", methods=["GET"])
def show_mojees():
    db = get_db()

    mojees = db.execute("SELECT STR_AGG(keyword) FROM mojees GROUP BY emoji").fetchall()

    mojees_json = []
    for m in mojees:
        mojees_json.append({"emoji": m[0], "keywords": m[1]})

    return jsonify(mojees)


@bp.route("/gallery/<int:image_id>/show")
def show_image(image_id):

    db = get_db()

    ids = db.execute("SELECT image_id from images").fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:
        path = db.execute(
            "SELECT path FROM images WHERE image_id = ?", (image_id,)
        ).fetchone()

        return path

    else:
        abort(404, "Image with ID {0} doesn't exist.".format(image_id))


@bp.route("/gallery/<int:image_id>/delete")
def delete_image(image_id):
    db = get_db()

    ids = db.execute("SELECT image_id from images").fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:
        db.execute("DELETE FROM images WHERE image_id == (?)", (image_id,))
        db.commit()
        return jsonify({"status": "success"})

    else:
        abort(404, "Image with ID {0} doesn't exist.".format(image_id))


@bp.route("/gallery/<filename>")
def return_pic(filename):
    return send_from_directory(
        current_app.config["UPLOAD_DIR"], secure_filename(filename)
    )
