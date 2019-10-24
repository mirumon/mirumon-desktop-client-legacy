isort --recursive  --force-single-line-imports app
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app  --exclude=__init__.py
black app
isort --recursive --multi-line=3 --trailing-comma --line-width 88 --force-grid-wrap=0 --combine-as app
