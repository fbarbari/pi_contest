#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit -1
fi

docker build . -t pi_contest

xhost +local:docker

docker run -it --rm \
    -e DISPLAY=${DISPLAY} \
    --volume="./the_scores.txt:/root/the_scores.txt" \
    --volume="${HOME}/.Xauthority:/root/.Xauthority:rw" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix" \
    --device /dev/input/event13 \
    --device /dev/input/event11 \
    pi_contest
