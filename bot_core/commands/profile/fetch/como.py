import asyncio
import os
from pathlib import Path
from pprint import pprint

import aiohttp

from config import objekt_contract




apollo_api = os.getenv('apollo_api')
AUTH_TOKEN = apollo_api


async def como(address: str, artist: str):
    base_url = f'https://apollo.cafe/api/user/by-address/{address}/como'

    url = f"{base_url}"
    headers = {
        'Authorization': AUTH_TOKEN
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:  # Request successful
                result = await response.json()
                new_dict = {}
                for i in result:
                    for k in range(len(list(result[i].keys()))):

                        if list(result[i].keys())[k] == objekt_contract[artist.lower()].lower():
                            new_dict[int(i)] = result[i][objekt_contract[artist.lower()].lower()]['count']

                return sum(new_dict.values()), new_dict

            else:  # Request failed
                print(
                    f"Failed request: Status {response.status}, Response: {await response.text()}")  # Debug: Print the error
                return None


if __name__ == '__main__':
    asyncio.run(como('0xeb3c27b01226271306cd29445790bc56b5e76eec', 'ARTMS'))