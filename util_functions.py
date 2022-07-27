import asyncio
import discord
import geoip2.database
import os
import random
import string
import threading

# Me
from global_config import ConfigManager
from logger import BotLogger

# lol
confmgr = ConfigManager("config.txt", False)
syslog = BotLogger("system_log.txt")

# <-------------- Don't touch pls --------------->
# If you're adding your own stuff, you need to look at
# global_config.py to see the supported data types, and add your
# own if needed.
# .get is string

PASTE_BASE = confmgr.get("PASTE_BASE")
PASTE_URL_BASE = confmgr.get("PASTE_URL_BASE")

HELP_LOC = confmgr.get("HELP_LOC")

WRONG_PERMS = confmgr.get("WRONG_PERMS")

NEW_MEMBER = confmgr.get("NEW_MEMBER")
INTRO_CHANNEL = confmgr.get("INTRO_CHANNEL")

DONT_SCARE = confmgr.get_as_list("NO_SCARY")

OWNER_ID = confmgr.get_as_int("OWNER_ID")

DEFAULT_STATUS_TYPE = confmgr.get("DEFAULT_STATUS_TYPE")
DEFAULT_STATUS_TEXT = confmgr.get("DEFAULT_STATUS_TEXT")

LIFX_IP = confmgr.get("LIFX_IP")
LIFX_MAC = confmgr.get("LIFX_MAC").replace("-", ":")

NAG_RECIEVER = confmgr.get("NAG_RECIEVER")

UNLOAD_COGS = confmgr.get_as_list("UNLOAD_COGS")
# <-------------- End --------------------->

WHITELIST = []


def fancy_msg(title, text, color, footnote=None):

    e = discord.Embed(colour=color)
    e.add_field(name=title, value=text, inline=False)

    if footnote is not None:
        e.set_footer(text=footnote)

    return e


def err_msg(title, text, footnote=None):
    return fancy_msg(title, text, discord.Colour.red(), footnote)


def warn_msg(title, text, footnote=None):
    return fancy_msg(title, text, discord.Colour.gold(), footnote)


def infmsg(title, text, footnote=None):
    return fancy_msg(title, text, discord.Colour.blurple(), footnote)


def image_embed(title, msg_type, dat):
    # see docs at
    # https://discordpy.readthedocs.io/en/stable/faq.html?highlight=embed#how-do-i-use-a-local-image-file-for-an-embed-image
    e = discord.Embed(color=discord.Colour.blurple())
    e.add_field(name="foo", value=title, inline=False)
    if msg_type == "rem":
        e.set_image(url=dat)
    else:
        e.set_image(url="attachment://" + dat)
    return e


# YouTube Stuff
async def get_yt_vid(link, song_name):
    syslog.log("Util-GetYTvid", "We're starting a download session")
    syslog.log("Util-GetYTvid", "Target filename is: " + song_name)

    await run_command_shell(
        "cd bin && python3 download_one.py " + link + " " + song_name + " && cd ../"
    )

    syslog.log("Util-GetYTvid", "All done!")


# Simple file wrappers
def check(fn):
    if os.path.exists(fn):
        return True
    else:
        return False


def save(fn, text):
    with open(fn, "a+") as f:
        f.write(text + "\n")


def get(fn):
    if check(fn):
        with open(fn) as f:
            return f.read()


def ensure(fn):
    if not check(fn):
        os.makedirs(fn, exist_ok=True)


def get_stamp():
    os.system("date >> stamp")
    with open("stamp") as f:
        s = f.read()
    os.remove("stamp")
    return s


def is_whitelisted(word):
    if word in WHITELIST:
        return True
    else:
        return False


def wrong_perms(command):
    syslog.log("System", "Someone just failed to run: '" + command + "'")
    return WRONG_PERMS.replace("{command}", command)


# Maybe add: https://docs.python.org/3/library/shlex.html#shlex.quote ?
async def run_command_shell(command, grc=False):
    """Run command in subprocess (shell)."""

    kill = lambda proc: proc.kill()
    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Status
    print("Started:", command, "(pid = " + str(process.pid) + ")", flush=True)

    kill_timer = threading.Timer(60, kill, [process])

    try:
        # Wait for the subprocess to finish
        kill_timer.start()
        stdout, stderr = await process.communicate()
    except:
        kill_timer.cancel()

    # Progress
    if process.returncode == 0:
        print("Done:", command, "(pid = " + str(process.pid) + ")", flush=True)
        # Result
        result = stdout.decode().strip()
    else:
        print("Failed:", command, "(pid = " + str(process.pid) + ")", flush=True)
        # Result
        result = stderr.decode().strip()

    kill_timer.cancel()

    if not grc:
        # Return stdout
        return result
    else:
        return process.returncode, result


async def isup(host):
    code, _ = await run_command_shell("ping -c 1 " + host)
    if code == 0:
        return True
    else:
        return False


def paste(text):
    n = 25
    fn = (
        "".join(
            random.choice(
                string.ascii_uppercase + string.digits + string.ascii_lowercase
            )
            for _ in range(n)
        )
        + ".html"
    )
    with open(PASTE_BASE + fn, "w") as f:
        f.write(text)
    return PASTE_URL_BASE + fn


def get_geoip(ip):
    with geoip2.database.Reader("GeoLite2-City.mmdb") as reader:
        try:
            response = reader.city(ip)
            return {
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }
        except Exception as e:
            return {"message": str(e)}
