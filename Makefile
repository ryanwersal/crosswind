.PHONY: install lock repl tests format lint lint-prod check-dead-code clean nuke

# Setup poetry virtual env
install:
	poetry install

# Lock poetry dependencies
lock:
	poetry lock

# Invoke Python repl in venv
repl:
	poetry run python

# Run all automated tests (unit, integration, etc)
tests:
	poetry run pytest

# Run code through formatters
format:
	poetry run black crosswind --exclude \data

# Lint all source code
lint:
	poetry run pylint --rcfile=.pylintrc crosswind

# Lint but only emit errors (for automated builds)
lint-prod:
	poetry run pylint --rcfile=.pylintrc --errors-only crosswind

# Check for dead code
check-dead-code:
	poetry run vulture --min-confidence 80 crosswind

# Typical (and default) clean that tries to avoid removing user created data that is gitignored
clean:
	git clean -xdfe .vscode

# Clean everything that is unversioned or gitignored
nuke:
	git clean -xdf
