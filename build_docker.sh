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

docker build -t gamerbot .