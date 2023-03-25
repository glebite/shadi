"""country_codes.py
"""
import sys
import requests
from bs4 import BeautifulSoup, SoupStrainer
import aiohttp
import asyncio


URL = "https://data.worldbank.org/country"


class Acquisition:
    """Acquisition
    """
    def __init__(self, url):
        """
        """
        self.url = url
        self.countries = {}

    async def acquire_main_page(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                data = await response.read()
                await asyncio.sleep(0.5)

        soup = BeautifulSoup(data, 'html.parser')

        for link in soup.find_all('a'):
            if not link['href'].endswith('country') and \
               'country' in link['href']:
                asyncio.run(self.get_country("https://data.worldbank.org" + link['href']))

    async def get_country(self, country_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(country_url) as response:
                data = await response.read()
                # await asyncio.sleep(0.1)
        print(country_url, len(data))


if __name__ == "__main__":
    x = Acquisition(URL)
    asyncio.run(x.acquire_main_page())
