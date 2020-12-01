from datetime import datetime
from gtts import gTTS
import asyncio
import discord
import os
import time
from config import CLIENT_ID

async def play(voice, filename):
    time.sleep(0.5)
    print("[{0}]: Start playing {1}".format(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        filename))
    try:
        voice.play(discord.FFmpegPCMAudio(filename))
        i = 0
        while (i < 5.0):
            if (not voice.is_playing() or not voice.is_connected()):
                break
            time.sleep(0.1)
            i += 0.1
            if (i // 1 >= 5.0):
                voice.stop()
                break
    except Exception as e:
        print("Error playing {0}".format(filename))
        voice.stop()
    print("[{0}]: Stopped {1}".format(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            filename))
    return

async def leave(voices, voice=None):
    if (len(voices) < 1 and voice == None):
        print("Not in voice")
        return
    try:
        if (voice == None):
            voice = voices[0]
        if (voice.is_playing()):
            voice.stop()
        await voice.disconnect(force=True)
        print("Left {0}".format(voice.channel))
    except Exception as e:
        print("Error trying to leave {0}: {1}".format(voice.channel, str(e)))

def tts(name):
    try:
        filename = "files/voice_{0}.mp3".format(name)
        if os.path.exists(filename):
            return filename
        msg = "Bonjour {0}".format(name)
        sound = gTTS(text=msg, lang='fr', slow=False)
        sound.save(filename)
        return filename
    except Exception as e:
        print("Error (tts)")

