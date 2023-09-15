#!/bin/bash
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Project folder: $WORKDIR"
cd $WORKDIR/local-assets
docker-compose up -d
cd ..
python manage.py migrate
