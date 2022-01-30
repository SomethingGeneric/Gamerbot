#!/bin/bash

if [[ "$1" == "gb" ]]; then
    export bottoken=$(cat ~/.gamerbot_token)
else
    export bottoken=$(cat ~/.testtube-token)
fi

python3 combo.py