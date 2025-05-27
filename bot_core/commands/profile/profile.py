from io import BytesIO

from bot_core import client, strings_to_choices, auto_complete
from config import ARTISTS
from utils import *
import db
from .make import image_maker

@client.tree.command(name="profile", description="profile")
@app_commands.choices(
    artist=strings_to_choices(ARTISTS),
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def profile(
    action: discord.Interaction,
    cosmo_id: Optional[str],
    artist: str,
):



    address, cosmo_id_input, discord_id = None, None, None

    if cosmo_id:
        if '|' in cosmo_id:
            cosmo_id_input = cosmo_id.split('|')[0]
            address = cosmo_id.split('|')[1]

        else:
            verify = cosmo_id_verify(action, cosmo_id)
            if '|' in verify:
                cosmo_id_input = verify.split('|')[0]
                address = verify.split('|')[1]

            else:
                return await action.response.send_message(verify)
    elif db.get_value(action.user.id).get('cosmo').get('address'):
        cosmo_id_input = db.get_value(action.user.id).get('cosmo').get('id')
        address = db.get_value(action.user.id).get('cosmo').get('address')

    await action.response.defer(ephemeral=False)

    img = await image_maker(address, artist, cosmo_id_input, discord_id)

    # 이미지 저장
    buffered_image = BytesIO()
    # img.save(buffered_image, format="webp", subsampling=10, quality=90)
    img.show()
    img.convert('RGB').save(buffered_image, format="jpeg", subsampling=10, quality=90)
    # img.save(buffered_image, format="png", optimize=False)
    buffered_image.seek(0)

    await action.followup.send(
        files=[discord.File(fp=buffered_image, filename=f"{action.user.id}.jpeg")]
    )



@profile.autocomplete("cosmo_id")
async def cosmo_id_autocomplete(
    interaction: discord.Interaction,
    current: str  # 사용자가 지금까지 입력한 텍스트
) -> list[app_commands.Choice[str]]:
    return auto_complete.cosmo_id(interaction, current)