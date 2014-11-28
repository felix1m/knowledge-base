#!/bin/bash

# on server first run 'sudo su'

while getopts ":r:h" opt; do
  case $opt in
    r)
      sudo su && echo "Running as root!"
      ;;
    h)
echo "Stops and removes all running docker containers. Then (re-)builds kb/head image and runs a detached container based on it.\n\nPass in -r to run as root."
      exit 1
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# untag current image
docker rmi kb/head:latest

# build and tag new images
docker build -t kb/head .

#kill all containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

docker run -d -p 80:80 kb/head

# remove untagged images
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")

# run latest tagged image
# docker run -v /home/core/app/:/home/app/ -p 80:5000 kb/head

# consider:
# do not load gem docu
# Make a file ~/.gemrc and put this in it:
# gem: --no-rdoc --no-ri

