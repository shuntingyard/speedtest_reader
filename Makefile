# use make for rapid development cycles
#
all: sdist

.PHONY: clean venv pull run test sdist upload

clean:
	rm -rf .venv
	rm -rf src/*.egg-info && rm -rf build rm -rf dist && rm -rf *.log*

venv: clean
	python -m venv .venv

pull: venv
	.venv/bin/python setup.py install

run: pull
	@echo Nothing to do for 'run'

test: pull
	.venv/bin/python setup.py test

sdist: test
	.venv/bin/python setup.py sdist

upload:
	sh -c ". .venv/bin/activate; pip install twine; twine upload dist/*; deactivate"
