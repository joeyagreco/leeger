@echo off

black --config=pyproject.toml .
autoflake --config=pyproject.toml .
