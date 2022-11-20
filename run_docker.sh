#!/usr/bin/env bash

if [[ ! -f .token ]]; then
  if [[ -f ~/.token ]]; then
    cp ~/.token .token
  else
    printf "Bot token: "
    read TK
    echo $TK > .token
  fi
fi

if [[ "$1" == "-d" ]]; then
  docker run -d -e SECRET_TOKEN="$(cat .token)" gamerbot
else
  docker run -e SECRET_TOKEN="$(cat .token)" gamerbot
fi