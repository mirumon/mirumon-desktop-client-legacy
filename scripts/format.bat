isort --recursive  --force-single-line-imports app
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app  --exclude=__init__.py
black app
isort --recursive  app
