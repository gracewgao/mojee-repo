from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    jsonify,
    g,
    abort,
    send_from_directory,
    current_app
)
from werkzeug.exceptions import abort
from .db import get_db

import time
import os
from hashlib import md5
from PIL import Image

from .vision import *

bp = Blueprint("images", __name__)


def check_extension(extension):
    return extension in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route("/gallery")
def gallery():

    images = g.db.execute(
        "SELECT image_id, detail FROM images ORDER BY created_on desc"
    ).fetchall()

    if not images:
        abort(404, "No images found.")
    else:
        images_json = []
        for i in images:
            images_json.append({"image_id": i[0], "detail": i[1]})

    return jsonify(images_json)


def add_pic(filename, detail):
    labels = vision_label(filename)

    cursor = g.db.cursor()
    images = cursor.execute("INSERT INTO images (detail, fname) VALUES (?, ?)", (detail, filename,))
    image_id = cursor.lastrowid

    for label, score in labels.items():
        g.db.execute(
            "INSERT INTO keywords_images (image_id, keyword, score) VALUES (?, ?, ?)",
            (int(image_id), str(label.lower()), int(score),)
        )

    g.db.commit()


@bp.route("/gallery/add", methods={"POST"})
def add_image():
    
    image_file = request.files["file"]

    try:
        names = image_file.filename.rsplit(".", 1)
        extension = names[1].lower()
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
        add_pic(filename, names[0])
    else:
        abort(404)
    return 'ok'


@bp.route("/gallery/search", methods={"GET"})
def search():

    images = g.db.execute("SELECT image_id, filename, detail FROM images").fetchall()

    json = request.get_json(force=True)
    emoji = json["emoji"]

    images_json = []

    # attempts to match keywords of image with emoji
    for i in images:
        filename = i[1]
        image_keywords = g.db.execute(
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

    json = request.get_json(force=True)
    emoji = json["emoji"]
    keyword = json["keyword"]

    g.db.execute("INSERT INTO mojees (emoji, keyword) VALUES (?, ?)", (emoji, keyword))
    g.db.commit()

    return jsonify({"status": "success"})


@bp.route("/mojees/delete", methods=["POST"])
def delete_mojee():

    json = request.get_json(force=True)
    emoji = json["emoji"]
    keyword = json["keyword"]

    g.db.execute(
        "DELETE from mojees WHERE" " emoji == (?) AND keyword == (?)", (emoji, keyword)
    )
    g.db.commit()

    return jsonify({"status": "success"})


@bp.route("/mojees", methods=["GET"])
def show_mojees():

    mojees = g.db.execute("SELECT STR_AGG(keyword) FROM mojees GROUP BY emoji").fetchall()

    mojees_json = []
    for m in mojees:
        mojees_json.append({"emoji": m[0], "keywords": m[1]})

    return jsonify(mojees)


@bp.route("/gallery/<int:image_id>/")
def show_image(image_id):

    ids = g.db.execute("SELECT image_id from images").fetchall()
    found = False
    for i in ids:
        if image_id == id[0]:
            found = True
            break

    if found:
        fname = g.db.execute(
            "SELECT fname FROM images WHERE image_id = ?", (image_id,)
        ).fetchone()
        return send_from_directory(current_app.config["UPLOAD_DIR"], fname)

    else:
        abort(404, "Image with ID {0} doesn't exist.".format(image_id))


@bp.route("/gallery/<int:image_id>/delete")
def delete_image(image_id):

    ids = g.db.execute("SELECT image_id from images").fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:
        g.db.execute("DELETE FROM images WHERE image_id == (?)", (image_id,))
        g.db.commit()
        return jsonify({"status": "success"})

    else:
        abort(404, "Image with ID {0} doesn't exist.".format(image_id))