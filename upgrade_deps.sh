#!/bin/bash
poetry cache clear pypi --all --no-interaction
poetry update
poetry lock
dephell deps convert --from=poetry --to=Pipfile
pipenv lock --pre