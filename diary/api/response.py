import aiohttp

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}


async def get_response(url: str,
                       cookies: dict,
                       headers: dict = HEADERS) -> aiohttp.ClientResponse:
    "Perform HTTP GET request."
    async with aiohttp.ClientSession(headers=headers, 
                                     cookies=cookies) as s:
        async with s.get(url) as response:
            return response


async def get_json_response(url: str,
                            cookies: dict,
                            headers: dict = HEADERS):
    "HTTP GET запрос. Возвращает результат в виде json"
    async with aiohttp.ClientSession(headers=headers, 
                                     cookies=cookies) as s:
        async with s.get(url) as response:
            return await response.json()


async def get_text_response(url: str,
                            cookies: dict,
                            headers: dict = HEADERS) -> str:
    "HTTP GET запрос. Возвращает результат в виде текста"
    async with aiohttp.ClientSession(headers=headers, 
                                     cookies=cookies) as s:
        async with s.get(url) as response:
            return await response.text()
