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
@click.option('-e', '--emoji', type=str, help='Filter gallery by emoji')
def show_gallery(emoji, name='show-gallery'):
    """View all pictures matching filter criteria"""

    table = Texttable()
    items = []
    headings = [['ID', 'DESCRIPTION']]

    response = requests.get(server_url + "/gallery", params={'emoji': emoji, 'keyword': keyword})
    response_json = response.json()

    try:

        for detail in response_json:
            items.append([detail['name'], str(detail['joint_id'])])

        if location:
            items = []
            for detail in response_json:
                if detail['location'].lower() == location.lower():
                    items.append([detail['name'], str(detail['joint_id'])])

        if min_rating:
            allowed_ids = []
            ratings_response = requests.get(server_url + "/images/ratings")
            ratings_json = ratings_response.json()

            for r in ratings_json:
                if r['rating'] >= min_rating:
                    allowed_ids.append(r['joint_id'])

            if len(items) != 0:
                for i in range(len(items)):
                    if int(items[i][1]) not in allowed_ids:
                        items.pop(i)
            else:
                for detail in response_json:
                    if detail['joint_id'] in allowed_ids:
                        items.append([detail['name'], str(detail['joint_id'])])

        if len(items) > 0:
            table.add_rows(headings + items)
            click.echo(click.style('YOUR IMAGES', bg='black', fg='white'))
            click.echo('\n' + table.draw())
            click.echo('\nUse command: `view [id]` to view the image.')
        else:
            click.echo(click.style('NO IMAGES FOUND',
                                   bg='red', fg='white')
                       )


    except IndexError:
        click.echo(click.style('NO IMAGES FOUND FOR YOUR SEARCH',
                               bg='red', fg='white')
                   )


@click.command()
@click.option('-e', '--emoji', type=str, help='See tags for a specific emoji')
def show_mojees(emoji, name='show-mojees'):
    """View custom mojee tags"""

    table = Texttable()
    items = []

    try:

        if emoji:
            headings = [['ID', 'KEYWORD']]
            # todo: get with emoji?
            response = requests.get(server_url + "/mojees/" + emoji)
            response_json = response.json()
            for mojee in response_json:
                items.append([mojee['mojee_id'], mojee['keyword']])
        else:
            headings = [['EMOJI', 'KEYWORDS']]
            response = requests.get(server_url + "/mojees/all")
            response_json = response.json()
            for mojee in response_json:
                items.append([mojee['emoji'], mojee['keywords'].join(', ')])
        
        if len(items) > 0:
            table.add_rows(headings + items)
            click.echo(click.style('CUSTOM MOJEES', bg='black', fg='white'))
            click.echo('\n' + table.draw())

            if emoji:
                click.echo('\nUse command: `delete-mojee [EMOJI] [KEYWORD]` to delete a mojee.')
            else:
                click.echo('\nUse command: `show-mojees --emoji [EMOJI]` to edit tags.')

        else:
            click.echo(click.style('NO MOJEES FOUND',
                                   bg='red', fg='white')
                       )

    except IndexError:
        click.echo(click.style('NO MOJEES FOUND',
                               bg='red', fg='white')
                   )                


@click.command()
@click.argument('src', type=str)
def add_image(src, name='add-img'):
    """Adds a new image to the repository"""

    while not os.path.isfile(src):
        src = click.prompt("Invalid file! Enter the file path of your image: ", type=str)

    detail = click.prompt("(Optional) Enter a description:", type=str)
   
    add_json = {}
    add_json['src'] = src
    add_json['detail'] = detail

    confirm = ''
    while not (confirm == 'Y') and not (confirm == 'N'):
        confirm = click.prompt('\nAdd ' + src + (' with description "' + detail + '"' if detail else '') + '?', type=str)

    if confirm == 'Y':
        response = requests.post(server_url + "/gallery/add", json.dumps(order_json))
        if response.ok:
            click.echo('Image successfully added!')
        else:
            click.echo('Uh-oh, something went wrong! Please try again.')
    else:
        click.echo("Cancelled")


@click.command()
@click.argument('id', type=str)
def delete_image(id, name='del-img'):
    """Deletes an image from the repository"""

    while not os.path.isfile(src):
        src = click.prompt("Invalid file! Enter the file path of your image: ", type=str)

    confirm = ''
    while not (confirm == 'Y') and not (confirm == 'N'):
        confirm = click.prompt('\nDelete ' + id + '?', type=str)

    if confirm == 'Y':
        delete_json = {'image_id': id}
        response = requests.post(server_url + "/gallery/" + id + "?", json.dumps(delete_json))
        if response.ok:
            click.echo('Image successfully deleted!')
        else:
            click.echo('Uh-oh, something went wrong! Please try again.')
    else:
        click.echo("Cancelled")


# @click.command()
# @click.option('--veggie', is_flag=True, help='Filter for vegetarian options')
# @click.argument('joint_id', type=int)
# def show_menu(joint_id, veggie, name='show-menu'):
#     """Show menu items for joint specified"""
#     response = requests.get(server_url + f"/images/{joint_id}/menu")
#     table = Texttable()
#     headings = [['Name', 'Toppings', 'S', 'M', 'L']]

#     # Will be true when the user passes a pizza joint ID that doesn't exist
#     if response.status_code == 404:
#         print("The pizza joint id that you passed doesn't exist")
#         exit(1)

#     response_list = response.json()
#     table_rows = []
#     for res in response_list:
#         S = '$' + format(res['prices'][0].get('M'), '.2f')
#         M = '$' + format(res['prices'][0].get('M'), '.2f')
#         L = '$' + format(res['prices'][0].get('L'), '.2f')
#         if veggie:
#             if res['vegetarian']:
#                 table_rows.append([res['name'], res['toppings'], S, M, L])
#         else:
#             table_rows.append([res['name'], res['toppings'], S, M, L])

#     table.add_rows(headings + table_rows)
#     click.echo('\n' + table.draw())
                                    

cli.add_command(add_image)
cli.add_comand(delete_image)
cli.add_command(show_gallery)
cli.add_commend(show_mojees)
