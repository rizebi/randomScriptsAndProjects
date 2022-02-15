# This is a small template for an Flask application, which accepts GETs at a specific location, and call behind the hood a function.

-> The deploy is on Docker, with Gunicorn as a Web Server.

-> This template also have IP limiter set up

#############################################################

Build the image:

docker build . -t flaskimage


Start the container with mounted volume:

docker run -p 80:8000 flaskimage

(-d = for detached)


Log in container, without starting the app:

docker run -it -p 80:8000 --entrypoint=/bin/sh flaskimage


Log in the running container:

docker exec -it d9397bb140f6


Test with param:

curl localhost/wordsplit?search_term=texthere


Test wirh JSON

curl -X GET -H "Content-type: application/json" -H "Accept: application/json" -d '{"search_term":"texthere"}' localhost/wordsplit
