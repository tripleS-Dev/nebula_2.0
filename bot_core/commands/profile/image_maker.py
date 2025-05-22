import fetcher

async def image_maker(address, artist):
    await fetcher.get_stats(address, artist)