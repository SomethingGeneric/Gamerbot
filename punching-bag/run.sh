#!/usr/bin/env bash

if [[ "$1" == "-d" ]]; then
  docker run punchingbag
else
  docker run -d punchingbag
fi
