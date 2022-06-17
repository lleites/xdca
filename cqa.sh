#!/bin/bash

set -e
set -o pipefail

poetry run topyn . --fix
poetry run pytest -rf tests

echo
echo "OK 👍"
