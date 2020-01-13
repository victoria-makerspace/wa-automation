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
### powershell
```sh
pipenv run python wap <args> <config file> -o <operation>
```
#### example
```sh
pipenv run python wap -c config -o cancel
```
### POSIX
```sh
pipenv run ./wap <args> <config file> -o <operation>
```
#### example
```sh
pipenv run ./wap -c config -o cancel
```

## TODOs

* Change the way errors raised in process of running the script are handled.
