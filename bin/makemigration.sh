#!/bin/bash
DIR="$( cd "$( dirname . )" && pwd )"
. ${DIR}/activate.sh
django-admin makemigrations "$@"