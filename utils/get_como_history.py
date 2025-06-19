import os

import requests
import json
import asyncio
import aiohttp
from decimal import Decimal
from typing import Literal


from config import como_contract, gravity_address, abstract_como_token_id

alchemy_api = os.getenv('alchemy_api')



async def get_total_tokens_sent(from_address: str, artist: str, network: Literal["abstract", "polygon"]):
    url = f"https://{network}-mainnet.g.alchemy.com/v2/{alchemy_api}"

    contract_address = como_contract[network][artist.lower()].lower()
    to_address = gravity_address[network][artist.lower()]
    if network == "abstract":
        category = 'erc1155'
    elif network == "polygon":
        category = 'erc20'
    else:
        return 'Error'

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    total_amount = 0
    page_key = None

    async with aiohttp.ClientSession() as session:
        while True:
            params = {
                "fromAddress": from_address,
                "toAddress": to_address,
                "contractAddresses": [contract_address],
                "category": [category],
                "excludeZeroValue": True,
                "withMetadata": False,
                "maxCount": "0x3e8"  # 한 번에 최대 1000개의 전송 내역 조회
            }
            if page_key:
                params['pageKey'] = page_key
            payload = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "alchemy_getAssetTransfers",
                "params": [params]
            }
            async with session.post(url, json=payload, headers=headers) as response:
                data = await response.json()
            #print(data)
            transfers = data.get('result', {}).get('transfers', [])
            for transfer in transfers:
                value_str = transfer['value']


                if value_str is None:
                    if not transfer['erc1155Metadata'][0]['tokenId'] == abstract_como_token_id[artist.lower()]:
                        continue

                    value_str = transfer['erc1155Metadata'][0]['value']

                    value_decimal = int(value_str, 0)
                    #print(value_decimal)
                    total_amount += value_decimal

                else:
                    value_str = transfer['value']
                    value_decimal = Decimal(value_str)
                    total_amount += value_decimal

            page_key = data.get('result', {}).get('pageKey', None)
            if not page_key:
                break  # 더 이상의 페이지가 없으면 종료

    return total_amount


if __name__ == "__main__":
    a = asyncio.run(get_total_tokens_sent('0x9526E51ee3D9bA02Ef674eB1E41FB24Dc2165380', 'tripleS', 'polygon'))
    print(a)