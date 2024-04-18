#!/bin/bash

RUN_TYPE="$1"
WORKSPACE=$(pwd)

PY_VENV="${WORKSPACE}/.venv"
PY_VENV_ACTIVATE="${PY_VENV}/bin/activate"
PY_REQ="${WORKSPACE}/requirements.txt"

export FLASK_APP="${WORKSPACE}/flask_endpoints.py"
source config
source "${PY_VENV_ACTIVATE}"

if [ "$RUN_TYPE" = "--compress" ]; then
    echo "Compress"
    python3 create_timelapse.py -f "${TIMELAPSE_FILE_EXTRA}"
else
    echo "Capture"
    flask run --host=0.0.0.0 -p 5000
fi

