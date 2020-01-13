# wa-automation

## Usage

This project uses [Pipenv](https://pipenv.kennethreitz.org/en/latest/) for
dependency management.

```sh
pipenv sync # Installs all depedencies.
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
