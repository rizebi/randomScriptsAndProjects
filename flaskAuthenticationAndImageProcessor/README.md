# devops-mission-rizebi

## Usage

First, we must login (see "Create new users" if no user is created)

Then upload the image, select from drop-down the filter and click button "Transform picture".

After that, the picture will be shown on the screen. Right click on it, and select "Save Image As" (no quality loss).

If you want to try another filter, click the browser "Back" button, and select different filter.


## Create new users

New users can be created from the /signup page. To create new users, an admin token must be entered. This admin token is set in ./image_processor/__init__.py. Search for "ADMIN_TOKEN_FOR_USER_CREATION".

## Deploy

1. Make sure python3 and pip3 are installed

sudo apt install -y python3 python3-pip

2. Install Python3 modules:

sudo pip3 install Flask Flask-Login Flask-SQLAlchemy pillow numpy

3. Get code, and go to directory.

git pull git@github.com:moul/devops-mission-rizebi.git

cd devops-mission-rizebi

4. Start application

sudo python3 app.py

To start in background:

nohup sudo python3 app.py &

Or start it as a service, and configure the service to start automatically at the start of the server (this depends on the OS)

## Few "architecutre" details

Application is written in Flask

Storage (users and passwords) are stored in SQLite

When a picture transformation is submitted, a bash script that will run the corresponding program will be invoked
