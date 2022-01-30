import youtube_dl, os, sys

filename = sys.argv[2] + ".mp3"
ytb_opts = {
    "newline": True,
    "ignoreerrors": True,
    "format": "best",
    "audio-format": "mp3",
    "outtmpl": filename,
}
ydl = youtube_dl.YoutubeDL(ytb_opts)
ydl.download([sys.argv[1]])
os.system("mv *.mp3 ../music/.")
