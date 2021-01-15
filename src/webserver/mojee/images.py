from flask import (
    Blueprint, request, redirect, url_for, jsonify
)
from werkzeug.exceptions import abort
from .db import get_db

bp = Blueprint('images', __name__)


@bp.route('/gallery')
def gallery():
    db = get_db()
    images = db.execute(
        'SELECT image_id, description FROM images'
    ).fetchall()

    if not images:
        abort(404, "No images found.")
    else:
        images_json = []
        for i in images:
            images_json.append(
                {
                    'image_id': i[0], 'desc': i[1]
                 }
            )

    return jsonify(images_json)


@bp.route('/gallery/search', methods={'GET'})
def search():

    db = get_db()
    images = db.execute(
        'SELECT image_id, description FROM images'
    ).fetchall()

    json = request.get_json(force=True)
    emoji = json['emoji']
    keywords = json['keyword']
    
    images = db.execute(
        'SELECT image_id, description FROM images'
    ).fetchall()
    
    images_json = []
    for i in images:
        images_json.append({'image_id': i[0], 'desc': i[1]})

    return jsonify(images_json)


@bp.route('/mojees/add', methods=['POST'])
def add_emoji():
    db = get_db()

    json = request.get_json(force=True)
    emoji = json['emoji']
    keyword = json['keyword']

    db.execute(
        'INSERT INTO mojees'
        ' VALUES (?, ?)',
        (emoji, keyword)
    )
    db.commit()

    return jsonify({"status": "success"})


@bp.route('/mojees/delete', methods=['POST'])
def delete_mojee():
    db = get_db()

    json = request.get_json(force=True)
    mojee_id = json['mojee_id']
    keyword = json['keyword']

    db.execute(
        'DELETE from mojees WHERE'
        ' mojee_id == (?)',
        (mojee_id)
    )
    db.commit()

    return jsonify({"status": "success"})


@bp.route('/mojees/all')
def ratings():
    db = get_db()
    mojees = db.execute(
        'SELECT mojee_id, keyword FROM mojees GROUP BY mojee_id'
    ).fetchall()

    mojees_json = []
    for mojee in mojees:
        mojees_json.append({'mojee_id': mojee[0], 'keywords': mojee[1]})

    return jsonify(ratings_json)


@bp.route('/gallery/<int:image_id>/show')
def show(image_id):

    db = get_db()

    ids = db.execute('SELECT image_id from images').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:
        path = db.execute(
            'SELECT path FROM images WHERE image_id = ?', (image_id,)
        ).fetchone()

        return jsonify(path)
    
    else:
        abort(404, "Image with ID {0} doesn't exist.".format(image_id))

@bp.route('/gallery/<int:image_id>/delete')
def delete_image(image_id):
    db = get_db()

    ids = db.execute('SELECT image_id from images').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break
    
    if found:
        db.execute(
            'DELETE FROM images WHERE image_id == (?)'
            (image_id,)
        )
        db.commit()
        return jsonify({"status": "success"})

    else:
        abort(404, "Image with ID {0} doesn't exist.".format(image_id))


@bp.route('/images/<int:joint_id>/menu')
def menu(joint_id):
    db = get_db()

    ids = db.execute('SELECT joint_id from images').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:
        pizzas = db.execute(
            'SELECT m.pizza_id, name, toppings, vegetarian, p.small, p.medium, p.large'
            ' FROM pizzas m JOIN prices p ON m.pizza_id = p.pizza_id'
            ' WHERE m.joint_id = ?',
            (joint_id,)
        ).fetchall()

        pizzas_json = []
        for p in pizzas:
            prices = []
            prices.append(
                {'S': p[4], 'M': p[5], 'L': p[6]}
            )
            pizzas_json.append(
                {
                    'pizza_id': p[0], 'name': p[1], 'toppings': p[2],
                    'vegetarian': bool(p[3]), 'prices': prices
                }
            )

        return jsonify(pizzas_json)

    else:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))


@bp.route('/images/<int:joint_id>/rate', methods=['POST'])
def rate(joint_id):
    db = get_db()

    ids = db.execute('SELECT joint_id from images').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:    
        json = request.get_json(force=True)
        rating = json['rating']
        review = json['review']
        joint_id = json['joint_id']

        db.execute(
            'INSERT INTO ratings'
            ' VALUES (?, ?)',
            (joint_id, rating)
        )
        db.commit()

        if review is not None:
            db.execute(
                'INSERT INTO reviews'
                ' VALUES (?, ?)',
                (joint_id, review)
            )
            db.commit()
        return jsonify({"status": "success"})

    else:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))

