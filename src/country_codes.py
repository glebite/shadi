"""country_codes.py

Retrieve the country information from the
worldbank site.

"""
import time
from bs4 import BeautifulSoup
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
        """acquire_main_page from the site to get the country data

        Parameters:
        n/a

        Returns:
        n/a
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                data = await response.read()
                await asyncio.sleep(0.5)

            soup = BeautifulSoup(data, 'html.parser')

            urls = []
            for link in soup.find_all('a'):
                if not link['href'].endswith('country') and \
                   'country' in link['href']:
                    urls.append("https://data.worldbank.org" + link['href'])

            tasks = [self.get_country(url, session) for url in urls]
            return await asyncio.gather(*tasks)

    async def get_country(self, country_url, session):
        """get_country - retrieve the country data

        Parameters:
        country_url (str): the url pointing to the country
        session (ClientSession): client session handed in

        Returns:
        n/a
        """
        async with session.get(country_url) as response:
            data = await response.read()
            country = country_url.split('/')[-1].split('?')[0]
            print(f'Getting {country=}')
            soup = BeautifulSoup(str(data), features='html5lib')
            for link in soup.find_all('a', href=True):
                if 'downloadformat=CSV' in link['href']:
                    print(country, link['href'])
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    x = Acquisition(URL)
    asyncio.run(x.acquire_main_page())
