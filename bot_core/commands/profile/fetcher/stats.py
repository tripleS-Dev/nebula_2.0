import asyncio
import os
from pprint import pprint

import aiohttp

apollo_api = os.getenv('apollo_api')
AUTH_TOKEN = apollo_api


async def get_stats(address: str, artist: str):
    base_url = f'https://apollo.cafe/api/user/by-address/{address}/stats'

    url = f"{base_url}"
    headers = {
        'Authorization': AUTH_TOKEN
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:  # Request successful
                result = await response.json()

                for one in result:
                    if one['artistName'] == artist.lower():
                        result_artist = one
                        break

                data = {
                    'total': sum(d['count'] for d in result_artist['classes']),
                    'members': top_three_stats(result_artist['members']),
                    'seasons': normalize_counts_integer(result_artist['seasons'])
                }
                #pprint(data)
                return data
            else:  # Request failed
                print(
                    f"Failed request: Status {response.status}, Response: {await response.text()}")  # Debug: Print the error
                return None


def top_three_stats(data):
    total = sum(item['count'] for item in data)
    # count 내림차순으로 정렬 후 상위 3개 선택
    top3 = sorted(data, key=lambda x: x['count'], reverse=True)[:3]
    # 결과 리스트 생성
    result = []
    for item in top3:
        pct = (item['count'] / total) * 100
        result.append({
            'name': item['name'],
            'count': item['count'],
            'percentage': int(round(pct, 0))  # 소수점 둘째 자리까지 반올림
        })
    return result

def normalize_counts_integer(data):
    total = sum(item['count'] for item in data)
    # 1) 원소별 raw 백분율
    raw_pcts = [item['count'] / total * 100 for item in data]
    # 2) 내림하여 정수 부분만 취함
    ints = [int(p) for p in raw_pcts]
    # 3) 남은 차이(100 - 합)만큼 배분
    remainder = 100 - sum(ints)
    # 4) 소수점 이하 부분을 구하고, 내림차순으로 정렬한 인덱스 목록
    fracs = [(raw_pcts[i] - ints[i], i) for i in range(len(data))]
    fracs.sort(reverse=True)
    # 5) 상위 remainder개 인덱스에 +1
    for _, idx in fracs[:remainder]:
        ints[idx] += 1
    # 6) 결과 리스트 생성 (원본 순서 유지)
    return [
        {'name': data[i]['name'], 'count': ints[i]}
        for i in range(len(data))
    ]


if __name__ == '__main__':
    asyncio.run(get_stats('0xAcb9f541D5F3A585500434f8A1D70864553415E7', 'tripleS'))