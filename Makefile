.PHONY: install update validate check repl tests format lint lint-prod check-dead-code clean nuke

# Setup poetry virtual env
install:
	poetry install

# Lock poetry dependencies
update:
	poetry update
	poetry lock

# Useful standin for the build process that tries to be similar for dev purposes
validate: check lint-prod tests

# Check attributes of the project
check:
	# Confirm lockfile is up to date
	poetry check

	# Confirm all imports are organized correctly
	poetry run isort --recursive --check-only .

	# Confirm no formatting changes are required
	poetry run black --check crosswind fixer_suites

	# Can we invoke crosswind at all?
	poetry run python crosswind/crosswind --help

	# Can we invoke crosswind for 2to3?
	poetry run python crosswind/crosswind --use-preset 2to3 crosswind/tests/acceptance/two.py

	# Can we invoke crosswind for 3to2?
	poetry run python crosswind/crosswind --use-preset 3to2 crosswind/tests/acceptance/three.py

# Invoke Python repl in venv
repl:
	poetry run python

# Run all automated tests (unit, integration, etc)
tests:
	poetry run pytest

# Run code through formatters
format:
	poetry run isort --recursive .
	poetry run black crosswind fixer_suites

# Lint all source code
lint:
	poetry run pylint --rcfile=.pylintrc crosswind fixer_suites

# Lint but only emit errors (for automated builds)
lint-prod:
	poetry run pylint --rcfile=.pylintrc --errors-only crosswind fixer_suites

# Check for dead code
check-dead-code:
	poetry run vulture --min-confidence 80 crosswind fixer_suites

# Typical (and default) clean that tries to avoid removing user created data that is gitignored
clean:
	git clean -xd --force --exclude .vscode

# Clean everything that is unversioned or gitignored
nuke:
	git clean -xd --force
