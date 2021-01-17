import random
import click
import requests
import json
import os.path
from texttable import Texttable


server_url = "http://127.0.0.1:5000"


@click.group()
def cli():
    pass


@click.command()
@click.option("-e", "--emoji", type=str, help="Filter gallery by emoji")
def show_gallery(emoji, name="show-gallery"):
    """View all pictures matching filter criteria"""

    table = Texttable()
    items = []
    headings = [["ID", "DESCRIPTION"]]

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
            click.echo(click.style("YOUR IMAGES", bg="black", fg="white"))
            click.echo("\n" + table.draw())
            click.echo("\nUse command: `view [id]` to view the image.")
        else:
            click.echo(click.style("NO IMAGES FOUND", bg="red", fg="white"))

    except IndexError:
        click.echo(click.style("NO IMAGES FOUND FOR YOUR SEARCH", bg="red", fg="white"))


@click.command()
@click.option("-e", "--emoji", type=str, help="See tags for a specific emoji")
def show_mojees(emoji, name="show-mojees"):
    """View custom mojee tags"""

    table = Texttable()
    items = []

    try:

        if emoji:
            headings = [["EMOJI", "KEYWORDS"]]
            response = requests.get(server_url + "/mojees")
            response_json = response.json()
            for mojee in response_json:
                items.append([mojee["emoji"], mojee["keywords"]])

        if len(items) > 0:
            table.add_rows(headings + items)
            click.echo(click.style("CUSTOM MOJEES", bg="black", fg="white"))
            click.echo("\n" + table.draw())
            click.echo(
                "\nUse command: `del-mojee [EMOJI] [KEYWORD]` to delete a mojee."
            )
            click.echo("\nUse command: `add-mojee [EMOJI] [KEYWORD]` to add a mojee")

        else:
            click.echo(click.style("NO MOJEES FOUND", bg="red", fg="white"))

    except IndexError:
        click.echo(click.style("NO MOJEES FOUND", bg="red", fg="white"))


@click.command()
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


@click.command()
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


@click.command()
@click.argument("src", type=str)
def add_image(src, name="add-img"):
    """Adds a new image to the repository"""

    while not os.path.isfile(src):
        src = click.prompt(
            "Invalid file! Enter the file path of your image: ", type=str
        )

    detail = click.prompt("(Optional) Enter a description:", type=str)

    confirm = ""
    while not (confirm == "Y") and not (confirm == "N"):
        confirm = click.prompt(
            "\nAdd "
            + src
            + (' with description "' + detail + '"' if detail else "")
            + "?",
            type=str,
        )

    if confirm == "Y":

        files = {"file": open(src, "rb")}
        values = {"detail": detail}
        response = requests.post(server_url + "/gallery/add", files=files, data=values)

        if response.ok:
            click.echo("Image successfully added!")
        else:
            click.echo("Uh-oh, something went wrong! Please try again.")
    else:
        click.echo("Cancelled")


@click.command()
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


cli.add_command(add_image)
cli.add_comand(delete_image)
cli.add_comand(show_mojees)
cli.add_command(show_gallery)
cli.add_comand(add_mojee)
cli.add_comand(delete_mojee)
