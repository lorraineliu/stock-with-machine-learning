#!/bin/bash
dir="$( cd "$( dirname . )" && pwd )"
p=$( dirname ${dir} )
cd "${p}"
export PYTHONPATH=${p}/venv/lib/python2.7
export DJANGO_SETTINGS_MODULE=stock.settings
export PYTHONPATH=$PYTHONPATH:$PWD
cd "${dir}"
atc_path="${p}/venv/bin/"
. ${atc_path}/activate
