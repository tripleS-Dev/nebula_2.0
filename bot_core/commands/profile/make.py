import asyncio
from pathlib import Path

from PIL import Image
from PIL.ImageDraw import ImageDraw
import fetcher
from image_maker import member_rank
from utils import paste_correctly, text_draw

BASE_DIR = Path(__file__).resolve().parent

async def image_maker(address, artist, cosmo_id, discord_id = None):
    data = {}
    images = {}
    base = Image.open(f"{BASE_DIR}/resources/base.png")

    draw = ImageDraw(base)
    nameplate(draw, cosmo_id, discord_id)

    data['stats'] =  await fetcher.get_stats(address, artist)


    if data.get('stats'):
        images['member_rank'] = member_rank(data['stats'])

    if images.get('member_rank'):
        base = paste_correctly(base, (49, 312), images['member_rank'])

    return base

def nameplate(draw, cosmo_id, discord_id):
    text_draw(draw, (434, 40), 'HalvarBreit-XBd.ttf', 45, cosmo_id, (255,255,255))
    text_draw(draw, (434, 80), 'HalvarBreit-XBd.ttf', 30, discord_id if discord_id else 'unknown', (88, 101, 242))

if __name__ == '__main__':
    a = asyncio.run(image_maker('0xAcb9f541D5F3A585500434f8A1D70864553415E7', 'tripleS', 'ILoveYouyeon', 'hj_sss'))
    a.show()