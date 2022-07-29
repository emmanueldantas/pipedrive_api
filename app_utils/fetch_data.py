import aiohttp
import asyncio
import os
import json
from app_utils.file_manager import save_to
from urllib.parse import urlencode

async def fetch_json(session, url):
    async with session.get(url) as response:
        data_stream = await response.json()
        try:
            return data_stream['data']
        except:
            print('Erro ao obter resultados de: ',data_stream)
            return None


async def retreive_tables(urls_batch, root_folder=r'pipe_api\files', save_as=None):  
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_json(session, url)) for url in urls_batch]
        responses = [record for records in await asyncio.gather(*tasks) if records for record in records]
        
        if save_as:
            file_path = os.path.join(root_folder, save_as)
            save_to(
                json.dumps(responses, indent=4), 
                file_path
            )
        return responses


class UrlGenerator:
    def __init__(self, endpoint=None, query_params=None, path_params=None, main_url=None) -> None:
        self.endpoint = endpoint
        self.main_url = main_url
        self.query_params = query_params
        self.path_params = path_params

    def generate_urls(self):
        try:
            return [self._url_generator(path_param) for path_param in self.path_params]
        except:
            return [self._url_generator(self.path_params)]

    def _url_generator(self, path_param): 
        endpoint = self.endpoint.format(path_param)
        url = f'{self.main_url}{endpoint}'
        if self.query_params:
            url_params = urlencode(self.query_params)
            url += f'?{url_params}'
        return url