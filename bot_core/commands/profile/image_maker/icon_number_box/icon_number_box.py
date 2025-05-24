from PIL import Image
from pathlib import Path

from PIL.ImageDraw import ImageDraw

from utils import round_square, text_size, paste_correctly, text_draw

BASE_DIR = Path(__file__).resolve().parent


def icon_number_box(icon_name, number):
    icon = Image.open(f"{BASE_DIR}/resources/{icon_name}.png")
    padding = 10

    match icon_name:
        case 'objekt':
            background_color = (135, 86, 255, 255)
            txt_color = (8,9,10)

        case 'como_triples':
            background_color = (231, 221, 255, 255)
            txt_color = (23,28,32)

        case _:
            background_color = (255, 255, 255, 255)
            txt_color = (0,0,0)


    x, *_ = text_size('HalvarBreit-XBd-5.ttf', 40, str(number))

    img = round_square(
        size=(x + padding * 2 + 5 + icon.size[0], 46),
        radii=(8, 8, 8, 8),  # (tl, tr, br, bl)
        color=background_color,
        iOS=True
    )

    img = paste_correctly(img, (padding, padding), icon)

    draw = ImageDraw(img)
    text_draw(draw, (padding+icon.size[0]+5, 10-1), 'HalvarBreit-XBd-5.ttf', 40, str(number), txt_color)

    return img


if __name__ == '__main__':
    a = icon_number_box('como_triples', 728)
    a.show()