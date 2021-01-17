## mojee

### :beginner: About
An image repository that allows you to search for images using emojis!

#### Technologies Used
- [`flask`](https://github.com/pallets/flask)
- [`$ click_`](https://github.com/pallets/click)
- [`sqlite3`](https://www.sqlite.org/index.html)
- [`google-cloud-vision`](https://cloud.google.com/vision)

### :electric_plug: Development Setup

- Clone this repository by running `git clone https://github.com/gracewgao/mojee.git` and cd into it.
- Make sure you have pipenv installed on your system. If not, do it by `pip install pipenv`.
- To activate a virtual environment for the project, run `pipenv shell`. After this, you'll be inside the virtual environment.
- Install the dependencies by running `pipenv install`.

### Running the webserver
- cd into the webserver directory using `cd src/webserver`.
- Run the command `flask run`.

### Setting up/Installing the CLI client
***Note: This can be done system wide (outside the pipenv) if you just want to use the client, but it's highly recommended to do it inside the virtual env for development.***
- In a new terminal window, cd into the cli directory by `cd src/cli`.
- Run the following command:
  - **Linux**: `python3 -m pip install --editable .`
  - **Windows & Mac**: `pip install -e .`
- Use any `mojee` command now!

### :zap: Usage
Type `mojee --help` to see a help message, and a list of commands you can use.<br>
***Type `mojee [command-name] --help` to see help for a particular command.***

#### Commands:
- `add-img` Add an image to the repo
- `del-img` Delete an image from the repo
- `show-gallery` View all images
- `add-mojee` Add a custom tag for an emoji
- `del-mojee` Add a custom tag for an emoji
- `show-mojees` View all your custom mojees
