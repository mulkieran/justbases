.PHONY: lint
lint:
	pylint setup.py	
	pylint src/justbases
	pylint tests

.PHONY: test
test:
	python3 -m unittest discover --verbose tests

.PHONY: coverage
coverage:
	coverage --version
	coverage run --timid --branch -m unittest discover tests/
	coverage report -m --fail-under=98 --show-missing --include="./src/*"

.PHONY: fmt
fmt:
	isort setup.py src tests
	black .

.PHONY: fmt-travis
fmt-travis:
	isort --diff --check-only setup.py src tests
	black . --check

PYREVERSE_OPTS = --output=pdf
.PHONY: view
view:
	-rm -Rf _pyreverse
	mkdir _pyreverse
	PYTHONPATH=src pyreverse ${PYREVERSE_OPTS} --project="justbases" src/justbases
	mv classes_justbases.pdf _pyreverse
	mv packages_justbases.pdf _pyreverse

.PHONY: archive
archive:
	git archive --output=./justbases.tar.gz HEAD

.PHONY: upload-release
upload-release:
	python setup.py register sdist upload

.PHONY: docs
docs:
	cd doc/_build/html; zip -r ../../../docs *

.PHONY: yamllint
yamllint:
	yamllint --strict .github/workflows/*.yml
