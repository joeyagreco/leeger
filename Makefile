.PHONY: deps
deps:
	@python3.10 -m pip install -r requirements.dev.txt
	@python3.10 -m pip install -r requirements.txt

.PHONY: fmt
fmt:
	@black --config=pyproject.toml .
	@autoflake --config=pyproject.toml .
	@isort .

.PHONY: fmt-check
fmt-check:
	@black --config=pyproject.toml . --check
	@autoflake --config=pyproject.toml . --check
	@isort . --check-only


.PHONY: test
test:
	@python3.10 -m pytest test/

.PHONY: reqs
reqs:
	@pipreqs --force --mode compat

.PHONY: pkg-build
pkg-build:
	@rm -rf build
	@rm -rf dist
	@python3.10 setup.py sdist bdist_wheel

.PHONY: pkg-test
pkg-test:
	@python3.10 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: pkg-prod
pkg-prod:
	@python3.10 -m twine upload dist/*