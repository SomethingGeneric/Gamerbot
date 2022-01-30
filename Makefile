pacman:
	sudo pacman -S git python-pip opus libffi curl traceroute whois figlet espeak ffmpeg nmap
apt:
	sudo apt install -y wget unzip python3-dev python3-pip git libopus-dev curl traceroute whois ffmpeg nmap
	mkdir -p ${HOME}/.local/bin
	sudo apt install -y figlet espeak
pip:
	pip3 install -r requirements.txt
