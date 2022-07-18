import discord
import asyncio


class DiscordTGTGBot:
    _client: discord.Client
    _token: str
    def __init__(self, token: str):
        self._client = discord.Client()
        self._token = token

    async def start(self):
        await self._client.start(self._token)

    async def wait_until_ready(self):
        await self._client.wait_until_ready()

    async def send(self, msg: str):
        for guild in self._client.guilds:
            guild: discord.Guild = guild
            channel: discord.TextChannel = guild.text_channels[0]
            await channel.send(msg)
