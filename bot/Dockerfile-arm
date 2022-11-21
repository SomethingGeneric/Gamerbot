FROM agners/archlinuxarm:latest
RUN pacman -Sy
RUN pacman -S --noconfirm --needed glibc libffi libsodium python-pynacl base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng ffmpeg bc gnu-netcat openssh
WORKDIR /bot
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir -p /root/.ssh
RUN echo "StrictHostKeyChecking no" > /root/.ssh/config
RUN mv /bot/gb /root/.ssh/id_rsa
RUN mv /bot/gb.pub /root/.ssh/id_rsa.pub
RUN chmod -R 600 /root/.ssh
CMD ["python3", "bot.py"]
