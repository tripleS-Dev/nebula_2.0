from bot_core import client, strings_to_choices, auto_complete
from config import ARTISTS
from utils import *
import db

@client.tree.command(name="nebula", description="setting")
@app_commands.choices(
    set_default_artist=strings_to_choices(ARTISTS),
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def nebula(
    action: discord.Interaction,
    set_cosmo_id: Optional[str],
    set_default_artist: Optional[app_commands.Choice[str]],
    set_title_objekt: Optional[bool],
):
    if set_default_artist:
        db.update_value(action.user.id, default_artist=set_default_artist.value)

    if set_cosmo_id:
        if '|' in set_cosmo_id:
            db.update_value(action.user.id, cosmo={'id': set_cosmo_id.split('|')[0], 'address': set_cosmo_id.split('|')[1]})
        else:
            verify = cosmo_id_verify(action, set_cosmo_id)
            if '|' in verify:
                db.update_value(action.user.id, cosmo={'id': verify.split('|')[0], 'address': verify.split('|')[1]})
            else:
                return await action.response.send_message(verify)

    await action.response.send_message(str(db.get_value(action.user.id)))



@nebula.autocomplete("set_cosmo_id")
async def cosmo_id_autocomplete(
    interaction: discord.Interaction,
    current: str  # 사용자가 지금까지 입력한 텍스트
) -> list[app_commands.Choice[str]]:
    return auto_complete.cosmo_id(interaction, current)