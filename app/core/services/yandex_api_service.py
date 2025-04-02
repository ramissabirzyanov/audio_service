import aiohttp


class YandexApiClient:

    async def _make_request(self, method: str, url: str, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()  
                return await response.json()

    async def get_yandex_token(self, url:str, code: str, client_id: str, client_secret: str) -> str:
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
         }
        response_data = await self._make_request("POST", url, data=data, headers=headers)
        return response_data["access_token"]

    async def get_user_email_by_yandex_token(self, url, access_token):
        headers={"Authorization": f"OAuth {access_token}"}
        response_data = await self._make_request("GET", url, headers=headers)
        return response_data["default_email"]
