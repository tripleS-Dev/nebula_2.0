import asyncio
from pathlib import Path

from PIL import Image
from PIL.ImageDraw import ImageDraw
import fetch
from image_maker import member_rank, nameplate, icon_number_box, como_calendar
from utils import paste_correctly, text_draw, round_square, text_size

BASE_DIR = Path(__file__).resolve().parent

async def image_maker(address, artist, cosmo_id, discord_id = None):
    data = {}
    images = {}
    base = Image.open(f"{BASE_DIR}/resources/base.png")


    data['stats'] =  await fetch.stats(address, artist)
    data['date'] = await fetch.singup_date(address, artist)
    data['como_count'], data['como_calendar'] = await fetch.como(address, artist)

    base = nameplate(base, cosmo_id, discord_id, data['date'])

    if data.get('stats'):
        images['member_rank'] = member_rank(data['stats'])

        if images.get('member_rank'):
            base = paste_correctly(base, (49, 312), images['member_rank'])


    if data.get('stats').get('total'):
        images['objekt_count'] = icon_number_box('objekt', data['stats']['total'])

        if images.get('objekt_count'):
            base = paste_correctly(base, (649-images['objekt_count'].size[0], 172), images['objekt_count'])


    if data.get('como_count'):
        images['como_count'] = icon_number_box(f'como_{artist.lower()}', data['como_count'])

        if images.get('como_count'):
            base = paste_correctly(base, (1271, 172), images['como_count'])

    if data.get('como_calendar'):
        images['calendar'] = como_calendar(data['como_calendar'])

        if images.get('calendar'):
            base = paste_correctly(base, (1291, 414), images['calendar'])

    base = paste_correctly(base, (1220, 96), Image.open(f"{BASE_DIR}/resources/bookmark/{artist.lower()}.png"))

    return base



if __name__ == '__main__':
    a = asyncio.run(image_maker('0xAcb9f541D5F3A585500434f8A1D70864553415E7', 'tripleS', 'ILoveYouyeon', 'hj_sss'))
    a.show()