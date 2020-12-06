import asyncio
import discord
import os
import time
import urllib.request
import urllib
import shutil

from discord.ext import commands
from datetime import datetime
from gtts import gTTS
from utils.config import CLIENT_ID
from utils.util import srs_only

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
        msg = urllib.parse.quote(msg)
        url = "https://translate.google.com/translate_tts?ie=UTF-8&q={0}&tl=fr-FR&client=tw-ob".format(msg)

        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        #urllib.request.urlretrieve(url, filename)
        #sound = gTTS(text=msg, lang='fr', slow=False)
        #sound.save(filename)
        return filename
    except Exception as e:
        print("Error (tts): {0}".format(e))


class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    @srs_only()
    async def on_voice_state_update(self, member, before, after):
        if (not member.bot and member.id != CLIENT_ID):
            if (after.channel != None and before.channel != after.channel):
                await leave(self.bot.voice_clients)
                filename = tts(member.display_name)
                try:
                    voice = await after.channel.connect()
                    print("Joined {0}".format(after.channel))
                    await play(voice, filename)
                    await leave(self.bot.voice_clients, voice)
                except discord.ClientException:
                    print("Error trying to join {0}: Already in voice".format(after.channel))
                    await leave(self.bot.voice_clients)
                except Exception as e:
                    print("Foo " + str(e))
                    await leave(self.bot.voice_clients)


def setup(bot):
    bot.add_cog(AnnounceCog(bot))
