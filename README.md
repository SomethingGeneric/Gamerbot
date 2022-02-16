# Gamerbot2
Discord bot with many functions
(It's a hot mess around here but it works)

## Note
The update function from git will not work unless you properly clone the repo and have some service like sytemd keeping the bot process alive (Example system-d unit is below)

## Setup
* Ensure you have git and pip
    * Arch Linux (and derivatives): `sudo pacman -S git python-pip`
    * Debian based: `sudo apt install python3-dev git -y`
* `pip3 install -r requirements.txt`
* Other requirements per cog (if you're going to disable a cog, you shouldn't need it's requirements):
    * Internet:
        * Arch: `sudo pacman -S curl traceroute whois nmap` 
        * Debian-based are probably the same
    * Memes:
        * Arch: `sudo pacman -S figlet`
        * Debian-based are probably the same
    * Speak:
        * Arch: `sudo pacman -S espeak-ng`
        * Debian-based are probably the same
    * Shells:
        * Install `notop` and `nofetch` from https://github.com/jnats
* Review things in config labeled `# NEED TO CHANGE`
* Put bot's token in the user's `~/.token`, and run ` python3 combo.py`
    * System-d service example:
        * Add to `/etc/systemd/system/<some_fn>.service`:
            ```
            [Unit]
            Description=Discord Bot
            After=network.target

            [Service]
            User=gamerbot
            WorkingDirectory=/home/gamerbot/Gamerbot2
            ExecStart=python3 combo.py
            Restart=always

            [Install]
            WantedBy=multi-user.target
            ```
        * `sudo systemctl daemon-reload && sudo systemctl enable --now <some_fn>`
        * If you ever have issues, `sudo systemctl status <some_fn>`
        
