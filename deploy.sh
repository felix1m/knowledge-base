#!/bin/bash

# deploy script for kb docker

    # options
    # -------

    # - local


    # run docker build
    # copy settings.cfg to /instance
    # docker run last image

    # - production

    # run docker build
    # copy settings.cfg to /instance
    # push to beanstalk
    # maybe more threads on uwsgi

# Colors
COLOR_OFF="\033[0m"   # unsets color to term fg color
RED="\033[0;31m"      # red
GREEN="\033[0;32m"    # green
YELLOW="\033[0;33m"   # yellow
MAGENTA="\033[0;35m"  # magenta
CYAN="\033[0;36m"     # cyan


STAGING_DIR="/home/app"
STAGING_BRANCH="master"

deploy_staging() {

  local branch=$2
  if [ -e $2 ]; then
    branch=$STAGING_BRANCH
  fi

  local commands="cd $STAGING_DIR &&\
    echo -e \"${YELLOW}--->${COLOR_OFF} Running Docker Build\" &&\
    docker run -i -t -p 80:80 91cbcbae279a &&\
    echo -e \"${YELLOW}--->${COLOR_OFF} Checking out branch ${branch}\" &&\
    git checkout ${branch} &&\
    echo -e \"${YELLOW}--->${COLOR_OFF} Pulling branch ${branch}\" &&\
    git pull origin ${branch} &&\
    echo -e \"${YELLOW}--->${COLOR_OFF} Gem: Bundle\" &&\
    bundle &&\

    echo -e \"${GREEN}DONE${COLOR_OFF}\" "

  ssh -T $STAGING_SSH_CONFIG $commands
}

case $1 in
  staging)
    echo "\n${GREEN}DEPLOYING APP TO STAGING${COLOR_OFF}\n"
    deploy_staging
    echo "\n${CYAN}APP DEPLOYED!${COLOR_OFF}\n"
    ;;
  production)
    echo "\n${RED}NO PRODUCTION YET :)${COLOR_OFF}\n"
    ;;
  *)
    echo "USAGE: $0 {staging|production}"
    exit
    ;;
esac
