FROM archlinux:latest
RUN pacman -Sy
RUN pacman -S --noconfirm --needed base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng ffmpeg bc gnu-netcat openssh
WORKDIR /bot
COPY . .
RUN pip3 install -r requirements.txt
RUN ssh-keygen -t rsa -q -f "$HOME/.ssh/id_rsa" -N ""
RUN echo "StrictHostKeyChecking no" >> "$HOME/.ssh/config"
CMD ["python3", "bot.py"]
