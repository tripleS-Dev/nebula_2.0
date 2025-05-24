from PIL.ImageDraw import ImageDraw
from PIL import Image
from utils import paste_correctly, text_draw, round_square, text_size




def nameplate(base, cosmo_id, discord_id, date):
    draw = ImageDraw(base)

    x, *_ = text_draw(draw, (434, 40), 'HalvarBreit-XBd.ttf', 45, cosmo_id, (255,255,255))
    x2, *_ = text_size('HalvarBreit-Bd.ttf', 24, date)

    img_out = round_square(
        size=(x2 + 10*2, 36),
        radii=(11, 11, 11, 11),  # (tl, tr, br, bl)
        color=(255, 255, 255, 255),
        iOS=True
    )
    img_in = round_square(
        size=(x2 + 10*2 - 3*2, 30),
        radii=(8, 8, 8, 8),  # (tl, tr, br, bl)
        color=(8, 9, 10, 255),
        iOS=True
    )

    base = paste_correctly(base, (434+x+7, 37), img_out)
    base = paste_correctly(base, (434+x+10, 40), img_in)

    draw = ImageDraw(base)

    text_draw(draw, (434+x+17, 40+7), 'HalvarBreit-Bd.ttf', 24, date, (255, 255, 255))

    text_draw(draw, (434, 80), 'HalvarBreit-XBd.ttf', 30, discord_id if discord_id else 'unknown', (88, 101, 242))

    return base