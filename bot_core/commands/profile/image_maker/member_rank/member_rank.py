import math

from PIL import Image
from PIL.ImageDraw import ImageDraw

from config import member_color
from utils import round_square, text_draw, text_size, paste_correctly, List, Dict
from pathlib import Path



def adjust_member_percentages_int(data, min_pct=0.15):
    """
    data: {'members': [{'count': int, 'name': str, 'percentage': float}, ...]}
    min_pct: 최소 비율 (0~1 사이), 기본값 0.15 (15%)

    'etc'까지 포함해 정수 퍼센트로 합이 정확히 100이 되도록 반환
    """
    # 1) 현 members 복사 및 etc 자동 추가
    members = [m.copy() for m in data['members']]
    total_pct = sum(m['percentage'] for m in members)
    if total_pct < 100:
        members.append({'count': None, 'name': 'etc', 'percentage': 100 - total_pct})

    # 2) 프랙션 계산
    fracs = [m['percentage'] / 100 for m in members]
    min_int = int(round(min_pct * 100))

    # 3) 고정 그룹 식별
    fixed = [f < min_pct for f in fracs]
    fixed_count = sum(fixed)
    fixed_total_int = fixed_count * min_int

    # 4) 나머지 그룹 스케일 계산
    remaining_int = 100 - fixed_total_int
    unfixed_fracs = [f for f, is_fixed in zip(fracs, fixed) if not is_fixed]
    orig_unfixed_sum = sum(unfixed_fracs)
    if orig_unfixed_sum <= 0:
        # 모든 항목이 고정된 경우
        return [{'name': m['name'], 'percentage': min_int} for m in members]
    scale = (1.0 - fixed_count * min_pct) / orig_unfixed_sum

    # 5) 스케일 적용 후 소수점 리스트
    raw_vals = []
    for f, is_fixed in zip(fracs, fixed):
        if is_fixed:
            raw_vals.append(min_int)
        else:
            raw_vals.append(scale * f * 100)

    # 6) 정수 분배 (Largest Remainder Method)
    floored = [math.floor(v) for v in raw_vals]
    remainder = 100 - sum(floored)
    # 소수 잔여치 계산
    remainders = [(i, raw_vals[i] - floored[i]) for i in range(len(floored))]
    # 잔여치 큰 순으로 인덱스 정렬
    remainders.sort(key=lambda x: x[1], reverse=True)

    result = floored[:]
    for i, _ in remainders[:remainder]:
        result[i] += 1

    # 7) 결과 매핑
    adjusted_members = []
    for m, pct in zip(members, result):
        adjusted_members.append({
            'count': m.get('count'),
            'name': m['name'],
            'percentage': pct
        })

    r1 = {'members': adjusted_members}
    # etc 항목 분리
    etc_item = next((m for m in r1['members'] if m['name'] == 'etc'), {'percentage': 0})

    # etc를 제외한 리스트
    filtered_members = [m for m in r1['members'] if m['name'] != 'etc']

    # 결과
    result = {
        'filtered_members': filtered_members,
        'etc_item': etc_item
    }

    return {'members': filtered_members}, etc_item['percentage']


BASE_DIR = Path(__file__).resolve().parent


def member_rank(data) -> Image.Image:
    blank = Image.new('RGBA', (600, 240), (0,0,0,0))
    etc_left = Image.open(f'{BASE_DIR}/resources/etc_left.png')
    etc_right = Image.open(f'{BASE_DIR}/resources/etc_right.png')
    etc_middle = Image.open(f'{BASE_DIR}/resources/etc_middle.png')
    line = Image.open(f'{BASE_DIR}/resources/line.png')
    etc_txt = Image.open(f'{BASE_DIR}/resources/etc_txt.png')
    num_txt = [1,2,3]
    num_txt[0] = Image.open(f'{BASE_DIR}/resources/1.png')
    num_txt[1] = Image.open(f'{BASE_DIR}/resources/2.png')
    num_txt[2] = Image.open(f'{BASE_DIR}/resources/3.png')

    #etc = 100 - sum(max(d['percentage'], 15) for d in data['members'])
    #etc = 100 - sum(max(d['percentage'], 15) for d in data['members'])

    data_refine, etc = adjust_member_percentages_int(data)


    pad = 0
    count = 0
    sums = 0
    pp = 100
    for member in data_refine['members']:
        sums += member['count']
        pp -= member['percentage']


        if count == 0:
            rounds = 16
        else:
            rounds = 0

        img = round_square(
            size=(600+pad, 240-40*count),
            radii=(rounds, 16, rounds, 32),  # (tl, tr, br, bl)
            color=member_color[member['name'].lower()],
            iOS=True if count == 0 else False
        )
        blank = paste_correctly(blank, (0, 40 * count), img)

        if 1000 <= member['count'] < 10000:
            count_font_size = 22
            x_offset = 0
            y_offset = 4
            padding = 4
        elif 10000 <= member['count']:
            count_font_size = 22
            x_offset = 9
            y_offset = 4
            padding = 2
        else:
            count_font_size = 30
            x_offset = 0
            y_offset = 0
            padding = 6


        x, y = text_size('HalvarBreit-XBd-5.ttf', count_font_size, str(member['count']))

        img = round_square(
            size=(x+padding*2, 30),
            radii=(6, 6, 6, 6),  # (tl, tr, br, bl)
            color=(8,9,10,255),
            iOS=True
        )
        blank = paste_correctly(blank, (600+pad-10-x-padding*2+x_offset, 200), img)

        draw = ImageDraw(blank)

        text_draw(draw, (600+pad-10-x-padding+x_offset, 205+y_offset), 'HalvarBreit-XBd-5.ttf', count_font_size, str(member['count']), (255,255,255))
        text_draw(draw, (600+pad-10, 175), 'HalvarBreit-XBd-5.ttf', 30, str(data['members'][count]['percentage'])+'%', (7,8,9), pos=2)
        text_draw(draw, (57, 10+40*count), 'HalvarBreit-XBd-5.ttf', 30, member['name'], (0,0,0))

        blank = paste_correctly(blank, (13 ,10+40*count), num_txt[count])

        count += 1
        pad -= member['percentage']*6 # if member['percentage'] >= 15 else 15*6



    if not etc <= 0:
        etc_middle_size = etc * 6 - 38

        if etc_middle_size < 90 - 38:
            etc_middle_size = 90 - 38

        etc_middle = etc_middle.resize((etc_middle_size, 120))

        blank.paste(etc_right, (22+etc_middle_size, 120), etc_right)
        blank.paste(etc_left, (0, 120), etc_left)
        blank.paste(etc_middle, (22, 120), etc_middle)
        blank.paste(etc_txt, (12, 130), etc_txt)


        etc_count = data['total'] - sums

        if 1000 <= etc_count < 10000:
            count_font_size = 22
            x_offset = 0
            y_offset = 4
            padding = 4
        elif 10000 <= etc_count:
            count_font_size = 22
            x_offset = 9
            y_offset = 4
            padding = 2
        else:
            count_font_size = 30
            x_offset = 0
            y_offset = 0
            padding = 6

        x, y = text_size('HalvarBreit-XBd-5.ttf', count_font_size, str(etc_count))


        img = round_square(
            size=(x + padding * 2, 30),
            radii=(6, 6, 6, 6),  # (tl, tr, br, bl)
            color=(42, 51, 58, 255),
            iOS=True
        )
        blank = paste_correctly(blank, (600+pad-10-x-padding*2+x_offset, 200), img)


        draw = ImageDraw(blank)

        text_draw(draw, (600+pad-10-x-padding+x_offset, 205+y_offset), 'HalvarBreit-XBd-5.ttf', count_font_size, str(etc_count), (23,28,32))
        text_draw(draw, (600+pad-10, 175), 'HalvarBreit-XBd-5.ttf', 30, str(pp)+'%', (42, 51, 58), pos=2)


    blank.paste(line, (0,160))

    return blank


if __name__ == '__main__':
    data = {'members': [{'count': 139, 'name': 'DaHyun', 'percentage': 70},
                        #{'count': 37, 'name': 'YeonJi', 'percentage': 10},
                        {'count': 34, 'name': 'YooYeon', 'percentage': 30}],
            'seasons': [{'count': 3, 'name': 'Atom01'},
                        {'count': 14, 'name': 'Binary01'},
                        {'count': 12, 'name': 'Cream01'},
                        {'count': 38, 'name': 'Divine01'},
                        {'count': 33, 'name': 'Ever01'}],
            'total': 376}

    member_rank(data).show()