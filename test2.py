import gtts

with open('himn.txt') as f:
    s = ""
    for i in range(52):
        s += f.readline()
    out = gtts.gTTS(text=s, lang='uk', slow=True)
    out.save('himn.mp3')
