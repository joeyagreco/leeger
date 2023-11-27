.PHONY: deps
deps: deps
	@python3.10 -m pip install -r requirements.dev.txt
	@python3.10 -m pip install -r requirements.txt

.PHONY: fmt
fmt:
	@black --config=pyproject.toml .
	@autoflake --config=pyproject.toml .
	@isort .

.PHONY: test
test:
	@python3.10 -m pytest test/

.PHONY: up-reqs
up-reqs:
	@pipreqs --force --mode compat