clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

deps:
	pip install -U setuptools
	pip install -r requirements-ci.txt

test:
	py.test -vvv

lint:
	pre-commit run -a -v

build: test
	python setup.py sdist
	python setup.py bdist_wheel

release: package_cloud clean build
	git rev-parse --abbrev-ref HEAD | grep '^master$$'
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`

dev:
	pip install -r requirements-dev.txt
