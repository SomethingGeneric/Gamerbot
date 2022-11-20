FROM archlinux:latest
RUN pacman -Sy
RUN pacman -S --noconfirm --needed figlet banner cowsay openssh
WORKDIR /stuff
COPY . .
CMD ["./do.sh"]
