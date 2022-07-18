import os
from datetime import datetime
from typing import Dict
import asyncio

from tgtg import TgtgClient
from dotenv import load_dotenv
from win10toast import ToastNotifier

from DiscordTGTGBot import DiscordTGTGBot
from TGTGManager import TGTGManager, Item


def show_msg(msg:str):
    toaster = ToastNotifier()
    toaster.show_toast("Too Good To Go", msg, duration=30, threaded=True)

def register(email: str):
    client = TgtgClient(email="mateusz.kisiel.mk@gmail.com")
    credentials = client.get_credentials()
    print(credentials)


async def watch():
    access_token = os.getenv('ACCESS_TOKEN')
    refresh_token = os.getenv('REFRESH_TOKEN')
    user_id = os.getenv('USER_ID')
    discrod_token = os.getenv("DISCORD_TOKEN")

    LATITUDE = 49.81075195446476
    LONGITUDE = 19.0938562251747
    RADIUS = 10

    discord_bot = DiscordTGTGBot(discrod_token)

    manager = TGTGManager(access_token, refresh_token, user_id)

    async def new_item_handler(item:Item):
        time = datetime.now().strftime("%H:%M:%S")
        msg = f"{time} --- New product {item.display_name} in {item.store.store_name} | {item.items_available} items avaliable\n"
        print(msg)
        await discord_bot.send(msg)

    manager.on_new(new_item_handler)

    async def watch():
        await discord_bot.wait_until_ready()
        await manager.watch(latitude=LATITUDE, longitude=LONGITUDE, radius=RADIUS, interval=5)

    await asyncio.gather(
        discord_bot.start(),
        watch()
    )

async def main():
    load_dotenv()
    await watch()


asyncio.run(main())
