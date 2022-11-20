FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng ffmpeg bc gnu-netcat
WORKDIR /bot
COPY .token /root/.
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]