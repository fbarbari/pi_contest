# pi_contest

<p align="center">
<img src="figure/pi_contest_logo_0.2.jpg" height=200 />
</p>

Educational game to estimate Greek π using "Monte Carlo" Method.

# How to use
## With `pip`
### Install requirements
```bash
pip3 install -r requirements.txt
```
### Run
```bash
./pi_contest
```

## With `poetry`
[`poetry`](https://python-poetry.org) is a useful Python build system and package manager. If you don't have it, you can install it with:
```bash
pip install poetry
```
### Install requirements
```bash
poetry install
```
### Run
```bash
poetry run ./pi_contest
```

## With `docker`
Alternatively, you can build a docker container using the provided `Dockerfile` with:
```bash
docker build . -t pi_contest
```
### Run
```bash
docker run -it --rm \
    -e DISPLAY=${DISPLAY} \
    --volume="${HOME}/.Xauthority:/root/.Xauthority:rw" \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    --device /dev/input/event13 \
    --device /dev/input/event11 \
    pi_contest
```
If it doesn't work, you may need to run
```bash
xhost +local:docker
```

# How to update dependencies
Currently, the dependencies of this project are mainly managed with `poetry`, which is also used to generate a `requirements.txt` file for `pip`.
First, regenerate the dependencies in the `poetry.lock` file with:
```bash
poetry update
```
Then, regenerate the `requirements.txt` file with:
```bash
poetry export -f requirements.txt -o requirements.txt
```
