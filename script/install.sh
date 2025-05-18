#!/bin/bash

pip install hatch
hatch new lintx

curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv --python=3.12
source .venv/bin/activate

uv pip install --project lintx .

uv build
uv pip install dist/lintx-0.0.1-py3-none-any.whl
