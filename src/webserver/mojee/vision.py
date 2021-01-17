from __future__ import print_function
from google.cloud import vision
import json

f = open('emoji-list.json')
file_data = json.load(f)
file_items = []
for k, v in file_data.items():
    for emoji_info in file_data[k]:
        file_items.append((emoji_info['emoji'], emoji_info['keywords']))
emojis = dict(file_items)

client = vision.ImageAnnotatorClient()


def vision_label(filename):

    file_name = os.path.join(
        os.path.dirname(__file__),
        filename)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
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


# test_uri = 'gs://cloud-samples-data/vision/using_curl/shanghai.jpeg'
# test_uri2 = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gettyimages-688899881-1519413300.jpg'
# test_labels = get_labels(test_uri2)
# for label, score in test_labels.items():
#         label_words = label.split()
#         for e, keywords in emojis.items():
#             for word in label_words:
#                 if word.lower() in keywords:
#                     print(e, word.lower())

# print('Labels (and confidence score):')
# print('=' * 30)
# for label, confidence in test_labels.items():
#     print(label, '(%.2f%%)' % (confidence*100.))

#test_search = input('Enter an emoji to search with:')