from __future__ import print_function
from google.cloud import vision
import json
import os
import io
from flask import current_app

f = open("mojee/emoji-list.json")
file_data = json.load(f)
file_items = []
for k, v in file_data.items():
    for emoji_info in file_data[k]:
        file_items.append((emoji_info["emoji"], emoji_info["keywords"]))
emojis = dict(file_items)
client = vision.ImageAnnotatorClient()


def vision_label(filename):

    file_name = os.path.join(os.path.join(current_app.config["UPLOAD_DIR"], filename))

    with io.open(file_name, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    labels = {}

    for label in response.label_annotations:
        # label confidence score out of 100
        labels[label.description] = label.score * 100

    return labels


def vision_match(labels, emoji):

    for label, score in labels.items():
        keywords = emojis[emoji]
        # if there is a match
        if label.lower() in keywords and score > 50:
            return True

    return False