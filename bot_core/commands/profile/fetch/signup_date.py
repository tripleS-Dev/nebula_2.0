import asyncio

import aiohttp



async def singup_date(address: str, artist):

    base_url = f'https://apollo.cafe/api/objekts/by-address/{address}'


    if artist.lower() == 'triples':
        artist = 'tripleS'
    else:
        artist = artist.lower()

    url = f"{base_url}?artist={artist}&sort=oldest"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:  # Request successful
                result = await response.json()
                return result['objekts'][0]['receivedAt'].split('T')[0]
            else:  # Request failed
                print(
                    f"Failed request: Status {response.status}, Response: {await response.text()}")  # Debug: Print the error
                return None


if __name__ == '__main__':
    asyncio.run(singup_date('0xAcb9f541D5F3A585500434f8A1D70864553415E7', 'triples'))