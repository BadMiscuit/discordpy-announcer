from datetime import datetime
from gtts import gTTS
import asyncio
import discord
import os
import time
from config import CLIENT_ID

async def announce(voice_clients, member, before, after):
    if (not member.bot and member.id != CLIENT_ID):
        if (after.channel != None and before.channel != after.channel):
            await leave(voice_clients)
            filename = tts(member.display_name)
            try:
                voice = await after.channel.connect()
                print("Joined {0}".format(after.channel))
                await play(voice, filename)
                await leave(voice_clients, voice)
            except discord.ClientException:
                print("Error trying to join {0}: Already in voice".format(after.channel))
                await leave(voice_clients)
            except Exception as e:
                print(str(e))
                await leave(voice_clients)

async def play(voice, filename):
    time.sleep(0.5)
    print("[{0}]: Start playing {1}".format(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        filename))
    voice.play(discord.FFmpegPCMAudio(filename))
    try:
        while True:
            if (not voice.is_playing() or not voice.is_connected()):
                break
            time.sleep(0.1)
    except Exception as e:
        print("Error playing {0}".format(filename))
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
    filename = "files/voice_{0}.mp3".format(name)
    if os.path.exists(filename):
        return filename
    msg = "Bonjour {0}".format(name)
    sound = gTTS(text=msg, lang='fr', slow=False)
    sound.save(filename)
    return filename


