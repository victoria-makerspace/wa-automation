# wa-automation

## Usage

This project uses [Pipenv](https://pipenv.kennethreitz.org/en/latest/) for
dependency management.

```sh
pipenv sync --dev # Installs all dependencies.
pipenv shell      # Open a shell within the virtual environment containing the
                  # dependencies. Alternatively, all commands could instead be
                  # preprended with `pipenv run`.
pylint wap *.py   # Run the linter against all Python files.
pytest            # Run all unit tests.
```

## TODOs

* Change the way errors raised in process of running the script are handled.
