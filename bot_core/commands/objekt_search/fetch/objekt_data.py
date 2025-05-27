import aiohttp


async def objekt_data(info):
    url = f"https://apollo.cafe/api/objekts/by-slug/{info['season'].lower()}-{info['member'].lower()}-{info['number']}{info['digital'].lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200: # 요청 성공
                result = await response.json()
                return result
            else: # 요청 실패
                print(f"Failed request: Status {response.status}, Response: {await response.text()}")  # Debug: Print the error
                return None