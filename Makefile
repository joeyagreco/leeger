.PHONY: deps
deps:
	@python -m pip install -r requirements.dev.txt
	@python -m pip install -r requirements.txt

.PHONY: fmt
fmt:
	@ruff check --fix
	@ruff format

.PHONY: fmt-check
fmt-check:
	@ruff check
	@ruff format --check

.PHONY: test
test:
	@python -m pytest test/

.PHONY: pkg-build
pkg-build:
	@rm -rf build
	@rm -rf dist
	@python setup.py sdist bdist_wheel

.PHONY: pkg-test
pkg-test:
	@python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: pkg-prod
pkg-prod:
	@python -m twine upload dist/*
