
from pathlib import Path

from PIL import Image, ImageDraw
from datetime import datetime
from zoneinfo import ZoneInfo
from utils import text_draw
from config import month_end, month_start, calender_colors


BASE_DIR = Path(__file__).resolve().parent


def como_calendar(data_count):


    x = 7  # Number of columns (days in a week)
    y = 5  # Number of rows (weeks in a month)

    # Load the day mask image
    day_mask = Image.open(f'{BASE_DIR}/resources/box.png')
    base = Image.new('RGBA', (day_mask.size[0] * x, day_mask.size[1] * y), (0, 0, 0, 0))


    # Set timezone to Asia/Seoul
    korean_timezone = ZoneInfo('Asia/Seoul')
    now_korean = datetime.now(korean_timezone)
    current_month = now_korean.month
    month_current = current_month



    days_in_month = month_end[month_current - 1]

    # Adjust data_count for days beyond the current month's end
    total_to_add = 0
    for day in list(data_count.keys()):
        if day > days_in_month:
            total_to_add += data_count[day]
            del data_count[day]

    if total_to_add > 0:
        data_count[days_in_month] = data_count.get(days_in_month, 0) + total_to_add

    # Generate the calendar image
    for row in range(y):
        for col in range(x):
            day_count = col + x * row + 1 - month_start[month_current - 1] + 2
            if day_count <= 0 or day_count > days_in_month:
                continue

            count = data_count.get(day_count, 0)
            rgb, rgb_txt = calender_colors[min(count, 5)]

            # Calculate the top-left corner of the day's box
            top_left = (col * day_mask.size[0], row * day_mask.size[1])
            day = Image.new('RGBA', day_mask.size, rgb)
            draw = ImageDraw.Draw(day)

            # Draw the day number
            text_draw(draw, (4, 5), 'HalvarBreit-XBd.ttf', 18, str(day_count), rgb_txt)

            # Paste the day image onto the base image
            base.paste(day, top_left, day_mask)

    return base

if __name__ == "__main__":
    #data_count = {29: 5, 11: 1, 23: 1, 7: 1, 5: 1, 6: 2, 12: 1, 16: 3, 26: 3, 27: 3, 15: 2, 17: 1, 19: 1, 20: 5, 8: 1, 9: 2, 22: 3, 25: 2, 3: 1, 30: 2, 1: 1}
    data_count = {1: 1, 3: 1, 4: 1, 7: 1, 9: 1, 11: 1, 12: 2, 13: 1, 17: 1, 19: 1, 20: 1, 21: 1, 23: 2, 24: 2, 26: 2, 29: 2, 30: 2}

    como_calendar(data_count).show()