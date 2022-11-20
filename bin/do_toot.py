#!/usr/bin/env python3

from mastodon import Mastodon
from random_word import RandomWords
from random import randint
import os, sys

url = sys.argv[1]
email = sys.argv[2]
passw = sys.argv[3]
volpath = sys.argv[4]
ccredpath = sys.argv[5]
ucredpath = sys.argv[6]
text = sys.argv[7]
un = sys.argv[8]
dc = sys.argv[9]

if not os.path.isfile(f"{volpath}/{ccredpath}"):
    r = RandomWords()
    w = r.get_random_word()
    Mastodon.create_app(
        f"gamerthebot-{w}-{str(randint(1, 10))}",
        api_base_url=url,
        to_file=f"{volpath}/{ccredpath}",
    )

mastodon = Mastodon(client_id=f"{volpath}/{ccredpath}")

mastodon.log_in(
    email,
    passw,
    to_file=f"{volpath}/{ucredpath}",
)

with open(f"{volpath}/post-log.txt", "a+") as f:
    f.write(f"User {un}#{str(dc)} posted: '{text}'\n")

res = mastodon.toot(f"{text} - {un}#{str(dc)}")

print(res["url"])
