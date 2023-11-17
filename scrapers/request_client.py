import httpx


client = httpx.AsyncClient()


async def close_client():
    await client.close()
