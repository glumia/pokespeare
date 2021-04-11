# pokespeare
Pokemon shakespearean descriptions

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).


## Local instance

Start the stack with Docker Compose:

```bash
docker-compose up
```

Now you can open your browser and interact with the API services of your application (they will be served at
`http://localhost:8000`).

## Development

Dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From project's root directory you can install all the development dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

**Make sure you execute all the commands that follow in this readme within that environment, otherwise your terminal
could complain about not finding the commands you provide him.**

Execute the following command to install git's *pre-commit* hooks:
```console
$ pre-commit install
```

This will make sure that all your changes are checked against Makefile's `lint` rule before committing (in this way
we avoid triggering a useless CI job).

### Tests

```console
$ make test
```

This will run the test suite and generate a coverage report (open `htmlcov/index.html` with your browser for a nice
web UI).

### Linting
```console
$ make lint
```
This will run various static analysis tools (*flake8*, *isort*, *black*, *safety*, *bandit*) to check for styling,
safety and dependencies vulnerabilities.


### Clean up development artifacts
To remove all the tests, coverage or other development artifacts (e.g. `__pycache__` directories) use:
```console
$ make clean
```

### Release
Use `bump2version` to generate a new release. It will take care of updating the `version` string where needed within the
project and create a new commit with those changes and a tag. 

```console
$ bump2version minor
```

Check bump2version's [README](https://github.com/c4urself/bump2version/blob/master/README.md) for more details about the
options you can provide to it.
