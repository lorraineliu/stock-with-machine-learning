#!/bin/bash
DIR="$( cd "$( dirname . )" && pwd )"
. ${DIR}/activate.sh
echo "Migrating database..."
django-admin migrate --noinput "$@"
