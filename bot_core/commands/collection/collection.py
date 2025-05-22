import db
from bot_core import client, strings_to_choices, auto_complete
from utils import *
from config import SEASONS, CLASSES, ARTISTS, SORTS



@client.tree.command(name="collection", description="Show cosmo collection")
@app_commands.choices(
    artist=strings_to_choices(ARTISTS),
)
@app_commands.rename(class_="class")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def collection(
    action: discord.Interaction,
    cosmo_id: Optional[str],
    discord_user: Optional[str],
    artist: Optional[app_commands.Choice[str]],
    season: Optional[str],
    class_: Optional[str]
):
    if not input_check(artist, SEASONS, season):
        return await action.response.send_message('season_error', ephemeral=True)
    elif not input_check(artist, CLASSES, class_):
        return await action.response.send_message('class_error', ephemeral=True)

    if not artist:
        if db.get_value(action.user.id) and db.get_value(action.user.id).get('default_artist'):
            artist = db.get_value(action.user.id).get('default_artist')

    if not cosmo_id and not discord_user:
        if not db.get_value(action.user.id) or not db.get_value(action.user.id).get('cosmo'):
            return await action.response.send_modal(cosmo_id_input())
        else:
            cosmo_id 



    await action.response.defer(ephemeral=False)


@collection.autocomplete("season")
async def item_autocomplete(
    interaction: discord.Interaction,
    current: str  # 사용자가 지금까지 입력한 텍스트
) -> list[app_commands.Choice[str]]:
    return auto_complete.choice_by_artist(interaction, current, SEASONS)

@collection.autocomplete('class_')
async def class_autocomplete(
        interaction: discord.Interaction,
        current: str
) -> list[app_commands.Choice[str]]:
    return auto_complete.choice_by_artist(interaction, current, CLASSES)


@collection.autocomplete('cosmo_id')
async def cosmo_id_autocomplete(
        interaction: discord.Interaction,
        current: str
) -> list[app_commands.Choice[str]]:
    return auto_complete.cosmo_id(interaction, current)



class cosmo_id_input(ui.Modal, title="Nebula"):
    name = ui.TextInput(label="cosmo id", placeholder="Jpark", max_length=16, style=discord.TextStyle.short)
    #remember = ui.Button(label="Remember this nickname")

    async def on_submit(self, action: discord.Interaction):
        verify = cosmo_id_verify(action, str(self.name))

        if '|' in verify:
            await action.response.send_message(f"{verify.split('|')[0]}", ephemeral=True)
        else:
            return await action.response.send_message(verify)