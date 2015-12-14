.PHONY: test
test: pep8
	py.test -v --cov=esengine -l --tb=short --maxfail=1 tests/

.PHONY: install
install:
	python setup.py develop

.PHONY: pep8
pep8:
	@flake8 esengine --ignore=F403

.PHONY: sdist
sdist: test
	@python setup.py sdist upload

.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
