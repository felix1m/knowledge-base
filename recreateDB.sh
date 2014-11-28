#!/bin/sh
#
# Recreate local database
#

usage() { echo "Usage: $0 [-h <mysql host>]" 1>&2; exit 1; }
error() { echo "FAILED: $1" ; exit 1; }

HOST='db_1'
while getopts "h:" o
do  case "$o" in
       h) HOST=${OPTARG};;
       *) usage;;
    esac
done
shift $((OPTIND-1))

echo "---> recreating database\n"
mysql -h "$HOST" -u root -e "drop database kb; create database kb;" || error 'could not empty db'

echo "---> migrating DB\n"
alembic upgrade head || error 'could not run db migrations'

echo "---> seeding DB\n"
python manage.py seed  || error 'could not seed db'



