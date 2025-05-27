from datetime import datetime
from utils import discord

def embed_generater(result, result_meta, setThumbnail=None):
    # Convert ISO date to Discord timestamp
    iso_date = result.get('createdAt')
    if iso_date:
        try:
            date_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            unix_timestamp = int(date_obj.timestamp())
            discord_timestamp = f"<t:{unix_timestamp}:D>"
        except ValueError:
            discord_timestamp = "Unknown date format"
    else:
        discord_timestamp = "Unknown"

    # Prepare embed fields
    accent_color = result.get('backgroundColor', '#FFFFFF').replace('#', '')
    print(accent_color)
    try:
        color_value = int(accent_color, 16)
    except ValueError:
        color_value = 0xFFFFFF  # Default white color

    collection_id = result.get('collectionId', 'Unknown')
    front_image_url = result.get('frontImage', '')

    copies = int(result_meta.get('total', '0'))
    description = result_meta.get('metadata', {}).get('description', '')
    if description:
        translated_description = description
    else:
        translated_description = 'No description available.'

    # Create the embed
    embed = discord.Embed(
        title="Objekt Information",
        color=color_value
    )
    if copies <= 10:
        rate = 'impossible'
    elif copies <= 25:
        rate = "extremely-rare"
    elif copies <= 50:
        rate = 'very-rare'
    elif copies <= 100:
        rate = 'rare'
    elif copies <= 350:
        rate = 'uncommon'
    else:
        rate = 'common'

    embed.set_author(name=collection_id)
    if setThumbnail:
        embed.set_thumbnail(url=front_image_url)
    else:
        embed.set_image(url=front_image_url)

    embed.add_field(name="Created at", value=discord_timestamp, inline=True)
    embed.add_field(name="Copies", value=str(copies) + f" ({rate})", inline=True)
    embed.add_field(name="Description", value=translated_description, inline=False)
    embed.set_footer(text="Powered by Apollo.cafe")
    return embed