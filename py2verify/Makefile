.PHONY: venv install update check tests format lint

# Create new Python 2.7 venv
venv:
	python2 -m virtualenv .venv

# Setup Poetry
install:
	poetry install

# Lock poetry dependencies
update:
	poetry update
	poetry lock

# Check attributes of the project
check:
	# Confirm lockfile is up to date
	poetry check

	# Confirm all imports are organized correctly
	poetry run isort --recursive --check-only .

# Run all automated tests
tests:
	poetry run pytest

# Run code through formatters
format: 
	poetry run isort --recursive .

# Lint all source code
lint:
	poetry run pylint --rcfile=../.pylintrc .