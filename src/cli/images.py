import random
import click
import requests
import json
import os.path
from texttable import Texttable
from PIL import Image

server_url = "http://127.0.0.1:5000"


@click.group()
def cli():
    pass


@cli.command()
@click.option("-e", "--emoji", type=str, help="Filter gallery by emoji")
def show_gallery(emoji, name="show-gallery"):
    """View all pictures matching filter criteria"""

    table = Texttable()
    items = []
    headings = [["ID", "NAME"]]

    response = ""
    if emoji:
        response = requests.get(
            server_url + "/gallery/search", json.dumps({"emoji": emoji})
        )
    else:
        response = requests.get(server_url + "/gallery")
    response_json = response.json()

    try:

        for image in response_json:
            items.append([image["image_id"], str(image["detail"])])

        if len(items) > 0:
            table.add_rows(headings + items)
            click.echo("YOUR IMAGES")
            click.echo("\n" + table.draw())
            click.echo("\nUse command: `show-image [ID]` to view the image.")
        else:
            click.echo("NO IMAGES FOUND")

    except IndexError:
        click.echo("NO IMAGES FOUND")


@cli.command()
@click.option("-e", "--emoji", type=str, help="See tags for a specific emoji")
def show_mojees(emoji, name="show-mojees"):
    """View custom mojee tags"""

    table = Texttable()
    items = []

    try:

        
        headings = [["EMOJI", "KEYWORDS"]]
        response = requests.get(server_url + "/mojees")
        response_json = response.json()
        for mojee in response_json:
            items.append([mojee["emoji"], mojee["keywords"]])

        if len(items) > 0:
            table.add_rows(headings + items)
            click.echo("CUSTOM MOJEES")
            click.echo("\n" + table.draw())
            
        else:
            click.echo("NO MOJEES FOUND")

    except IndexError:
        click.echo("NO MOJEES FOUND")

    click.echo("Use command: `del-mojee [EMOJI] [KEYWORD]` to delete a mojee.")
    click.echo("Use command: `add-mojee [EMOJI] [KEYWORD]` to add a mojee")



@cli.command()
@click.argument("emoji", type=str)
@click.argument("keyword", type=str)
def add_mojee(emoji, keyword, name="add-mojee"):
    """Adds a custom mojee tag"""
    mojee_json = {"emoji": emoji, "keyword": keyword}
    response = requests.post(server_url + "/mojees/add", json.dumps(mojee_json))
    if response.ok:
        click.echo(emoji + " successfully added!")
    else:
        click.echo("Uh-oh, something went wrong! Please try again.")


@cli.command()
@click.argument("emoji", type=str)
@click.argument("keyword", type=str)
def delete_mojee(emoji, keyword, name="add-mojee"):
    """Adds a custom mojee tag"""
    mojee_json = {"emoji": emoji, "keyword": keyword}
    response = requests.post(server_url + "/mojees/delete", json.dumps(mojee_json))
    if response.ok:
        click.echo(emoji + " successfully deleted!")
    else:
        click.echo("Uh-oh, something went wrong! Please try again.")


@cli.command()
@click.argument("src", type=str)
def add_image(src, name="add-img"):
    """Adds a new image to the repository"""

    while not os.path.isfile(src):
        src = click.prompt(
            "Invalid file! Enter the file path of your image", type=str
        )

    # detail = click.prompt("(Optional) Enter a description", type=str)

    confirm = ""
    while not (confirm == "Y") and not (confirm == "N"):
        confirm = click.prompt(
            "\nAdd "
            + src
            # + (' with description "' + detail + '"' if detail else "")
            + "? (Y/N)",
            type=str,
        )

    if confirm == "Y":

        files = {"file": open(src, "rb")}
        # values = {"detail": detail}
        response = requests.post(server_url + "/gallery/add", files=files)
        # response = requests.post(server_url + "/gallery/add", files=files, json=json.dumps(values))

        if response.ok:
            click.echo("Image successfully added!")
        else:
            click.echo("Uh-oh, something went wrong! Please try again.")
    else:
        click.echo("Cancelled")


@cli.command()
@click.argument("image_id", type=str)
def delete_image(image_id, name="del-img"):
    """Deletes an image from the repository"""

    while not os.path.isfile(src):
        src = click.prompt(
            "Invalid file! Enter the file path of your image: ", type=str
        )

    confirm = ""
    while not (confirm == "Y") and not (confirm == "N"):
        confirm = click.prompt("\nDelete " + image_id + "?", type=str)

    if confirm == "Y":
        delete_json = {"image_id": image_id}
        response = requests.post(
            server_url + "/gallery/" + image_id + "?", json.dumps(delete_json)
        )
        if response.ok:
            click.echo("Image successfully deleted!")
        else:
            click.echo("Uh-oh, something went wrong! Please try again.")
    else:
        click.echo("Cancelled")


@cli.command()
@click.argument("id", type=int)
def show_image(id, name="show-image"):
    """Display an image"""
    image = requests.get(server_url + "/gallery/" + str(id))
    print(type(image))
    # im = Image.open(image)  
    # im.show()

