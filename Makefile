.PHONY: clean clean-test clean-pyc clean-build

clean: clean-build clean-pyc clean-test # remove all artifacts

clean-build: # remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-pyc: # remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test: # remove test and coverage artifacts
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -fr htmlcov/
	@rm -fr .pytest_cache
	@rm -fr report.xml report.html

lint: # static code analysis
	flake8 pokespeare tests --max-line-length 88 # 88 is black's default
	isort --check --profile black --multi-line 3 .
	black --check .
	safety check --bare
	bandit -r pokespeare

test: clean # run test suite and generate coverage artifacts
	coverage run --source=pokespeare --omit=pokespeare/__init__.py -m pytest
	coverage report -m --fail-under 100
	coverage html
