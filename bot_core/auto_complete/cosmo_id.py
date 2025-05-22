import requests
from discord import Interaction

from utils import *
import aiohttp
import difflib


def cosmo_id(action: Interaction, name: str) -> list[app_commands.Choice[str]]:
    """apollo.cafe 사용자 검색(동기 버전)"""
    if '|' in name:
        return [app_commands.Choice(name="Cannot use '|'", value='0')]


    # 1) 길이 검증
    if len(name) < 4:
        return [app_commands.Choice(name="Enter at least 4 characters", value='0')]

    url = f"https://apollo.cafe/api/user/v1/search?query={name}"

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            users = result.get("results", [])

            if users:
                # 2) 닉네임 유사도 계산
                def similarity(nickname: str) -> float:
                    return difflib.SequenceMatcher(None, name.lower(), nickname.lower()).ratio()

                # 3) 유사도 기준 정렬 & 상위 25명 추출
                sorted_users = sorted(
                    users,
                    key=lambda user: similarity(user.get("nickname", "")),
                    reverse=True,
                )[:25]

                # 4) Choice 리스트로 변환
                return [
                    app_commands.Choice(name=user["nickname"], value=user["nickname"]+'|'+user["address"])
                    for user in sorted_users
                ]
    except requests.RequestException as err:
        # 네트워크 예외 처리
        print(f"[cosmo_id] Request failed: {err}")

    # 검색 실패(또는 예외) 시 기본 응답
    return [app_commands.Choice(name="User not found", value="User not found")]