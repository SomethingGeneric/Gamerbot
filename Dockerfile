FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng bc
WORKDIR /bot
COPY .token /root/.
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]