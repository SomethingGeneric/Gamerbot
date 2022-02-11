#!/bin/bash

if [[ "$1" == "gb" ]]; then
    cat ~/.gamerbot_token > ~/.token
else
    cat ~/.testtube-token > ~/.token
fi

python3 combo.py