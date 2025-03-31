import aiohttp


class YandexApiService:

    async def _make_request(self, method: str, url: str, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(self, method, url, **kwargs) as response:

                return await response.json()

    async def get_yandex_token(self, url:str, code: str, cliet_id: str, client_secret: str) -> str:
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": cliet_id,
            "client_secret": client_secret,
        }
        response = await self._make_request("POST", url, data=data)
        response.raise_for_status()
        return await response["access_token"]

    async def get_user_email_by_yandex_token(self, url, access_token):
        headers={"Authorization": f"OAuth {access_token}"}
        response = await self._make_request("GET", url, headers=headers)
        response.raise_for_status()
        return await response["default_email"]
