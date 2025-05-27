import db
from bot_core import client
from utils import *
from .text_sort import extract
from . import fetch
from .embed_generater import embed_generater

@client.tree.command(name="objekt_search", description="Search objekt")
@app_commands.describe(text='ex) seoyeon aa108 | s1 b102a')
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def objekt_search(
    action: discord.Interaction,
    text: str
):
    await action.response.defer(ephemeral=False)


    sorted_json = extract(text)
    print(sorted_json)
    for key in sorted_json.keys():
        print(key, sorted_json[key])

        if not sorted_json[key]:
            await action.followup.send(f"{key} is not found")
            return

    result_meta = await fetch.objekt_meta(sorted_json)

    result = await fetch.objekt_data(sorted_json)

    embed = embed_generater(result, result_meta)

    await action.followup.send(sorted_json, embed=embed)