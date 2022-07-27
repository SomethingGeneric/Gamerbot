# Gamerbot2
Discord bot with many functions

## Setup
* Ensure you have git and pip
    * Arch Linux (and derivatives): `sudo pacman -S git python-pip`
    * Debian based: `sudo apt install python3-dev git -y`
* `pip3 install -r requirements.txt`
* Other requirements per cog (if you're going to disable a cog, you shouldn't need it's requirements):
    * Internet & Shells:
        * Arch: `sudo pacman -S curl traceroute whois nmap wget` 
        * Debian-based are probably the same
    * Memes:
        * Arch: `sudo pacman -S figlet`
        * Debian-based are probably the same
    * Speak:
        * Arch: `sudo pacman -S espeak-ng`
        * Debian-based are probably the same
    * Shells:
      * For non-priv, you need `docker`, and the user running the bot needs to be able to use `docker run` without `sudo`
* Review things in config labeled `# NEED TO CHANGE`
* Put bot's token in the user's `~/.token`, and run `python3 combo.py`
    * System-d service example:
        * Add to `/etc/systemd/system/<some_fn>.service`:
            ```
            [Unit]
            Description=Discord Bot
            After=network.target

            [Service]
            User=gamerbot
            WorkingDirectory=/home/gamerbot/Gamerbot2
            ExecStart=python3 bot.py
            Restart=always

            [Install]
            WantedBy=multi-user.target
            ```
        * `sudo systemctl daemon-reload && sudo systemctl enable --now <some_fn>`
        * If you ever have issues, `sudo systemctl status <some_fn>`
        
