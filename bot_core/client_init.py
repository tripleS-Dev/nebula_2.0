from utils import *

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('Nebula'), intents=discord.Intents()) #intents=discord.Intents().all()

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged in as {self.user}')

        for guild in client.guilds:
            print(f'서버: {guild.name} (멤버 수: {guild.member_count})')


client = Client()
