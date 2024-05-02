#!/bin/bash

RUN_TYPE="$1"
WORKSPACE=$(pwd)

PY_VENV="${WORKSPACE}/.venv"
PY_VENV_ACTIVATE="${PY_VENV}/bin/activate"

export FLASK_APP="${WORKSPACE}/flask_endpoints.py"
source config
# shellcheck source=.venv
source "${PY_VENV_ACTIVATE}"

if [ "$RUN_TYPE" = "--compress" ]; then
    echo "Compress"
    python3 create_timelapse.py -f "${TIMELAPSE_FILE_EXTRA}" -u "${URL_UPLOAD}"
else
    echo "Capture"
    flask run --host=0.0.0.0 -p 5000
fi
