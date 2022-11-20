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
  docker run -d -v gamerbot-store:/gb-data -e SECRET_TOKEN="$(cat .token)" -e MASTODON_URL="https://social.xhec.dev" -e MASTODON_EMAIL="$(cat .m_email)" -e MASTODON_PASSWORD="$(cat .m_password)" gamerbot
else
  docker run -v gamerbot-store:/gb-data -e SECRET_TOKEN="$(cat .token)" -e MASTODON_URL="https://social.xhec.dev" -e MASTODON_EMAIL="$(cat .m_email)" -e MASTODON_PASSWORD="$(cat .m_password)" gamerbot
fi