FROM ubuntu:22.04

RUN cd \
    && apt update \
    && apt upgrade -y \
    && apt install -y python3 python3-pip libmtdev-dev libgl1-mesa-dev xclip \
    && pip3 install poetry \
    && mkdir -p -m 0700 /run/user/0

ENV XDG_RUNTIME_DIR=/run/user/0

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install \
    && chmod +x `poetry env info -p`/bin/garden \
    && poetry run garden install matplotlib

COPY . .

CMD poetry run python3 ./pi_contest
