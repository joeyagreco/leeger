@echo off

cd test
coverage run -m pytest
coverage xml -o coverage.xml
coverage html
cd ..
