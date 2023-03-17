import discord
from discord.ext import commands
import time
from pynput.keyboard import Key, Controller
import pygetwindow as gw
import pyautogui
from dotenv import load_dotenv
from os import environ
load_dotenv('TOKEN.env')
token = environ["TOKEN"]
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def open_and_screenshot():
    keyboard = Controller()
    # presses the window button and runs war thunder
    keyboard.press(Key.cmd)
    keyboard.press('r')
    keyboard.release(Key.cmd)
    keyboard.release('r')
    time.sleep(5)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # waits for update if there is one
    time.sleep(60)

    # gets current window and focuses it
    warthunder_window = gw.getWindowsWithTitle('War Thunder')[0]
    warthunder_window.restore()

    # waits for game to fully initialize onced focused
    time.sleep(20)
    pyautogui.screenshot('./warthunder.png')
    time.sleep(10)

    # collects the reward
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(5)
    warthunder_window.close()


@bot.event
async def on_ready():
    print('ready for the grind')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print('error', e)


@bot.tree.command(name='getreward', description='login to warthunder and fetch a reward')
async def getreward(interaction: discord.Interaction):
    try:
        channel = interaction.channel
        await interaction.response.send_message('Logging in and fetching reward')
        open_and_screenshot()
        embed = discord.Embed(title='Screenshot', color=discord.Color.random())
        file = discord.File('warthunder.png', filename='warthunder.png')
        embed.set_image(url="attachment://warthunder.png")
        await channel.send(embed=embed, file=file)
    except Exception as e:
        print('error', e)


bot.run(token)
