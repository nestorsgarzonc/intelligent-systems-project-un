from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

from scrapping import Attraction

BASE_URL = 'https://www.tripadvisor.co'
MAX_PAGES = 20
BASE_PAGE_NUMBER = 30


class AttractionsByCity:
    def __init__(self, name: str, url: str, city: str) -> None:
        self.name = name
        self.url = url
        self.city = city

    def __str__(self):
        return f'AttractionsByCity( {self.name},  {self.url},  {self.city})'


class TripAdvisorAttractionsScrapper:
    def __init__(self, path, url) -> None:
        self.driver: Chrome = webdriver.Chrome(ChromeDriverManager().install())
        self.attractions_urls: list[AttractionsByCity] = []

    def get_site_attractions(self, city_path: str, city_name: str):
        url = f'{BASE_URL}{city_path}'
        try:
            self.driver.get(url)
            time.sleep(2)
            print('Getting attractions')
            sections = self.driver.find_elements(
                By.XPATH,
                '/html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section'
            )
            print(f'For city {city_name} found {len(sections)} sections')
        except:
            print(f'Error getting attractions {city_path}')
        for raw_item in sections:
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", raw_item
            )
            time.sleep(0.2)
            tags = raw_item.find_elements(
                By.TAG_NAME,
                'a'
            )
            for tag in tags:
                try:
                    if ('/Attraction_Review' in tag.get_attribute('href')):
                        self.attractions_urls.append(
                            AttractionsByCity(
                                tag.text,
                                tag.get_attribute('href'),
                                city_name
                            )
                        )
                except:
                    pass
            print(
                f'For city {city_name} found {len(self.attractions_urls)} attractions'
            )
            print(self.attractions_urls)

    def get_attractions(self):
        for page in range(MAX_PAGES):
            self.get_site_attractions(
                f'/Attractions-g294074-Activities-oa{page* BASE_PAGE_NUMBER}-Bogota.html',
                'Bogota'
            )
        self.to_csv('Bogota')

    def to_csv(self, city_name: str):
        df = pd.DataFrame(
            [
                [attraction.name, attraction.url, attraction.city]
                for attraction in self.attractions_urls
            ],
            columns=['name', 'url', 'city']
        )
        df.to_csv(f'attractions_{city_name}.csv', index=False)

    def __str__(self) -> str:
        return f'TripAdvisorAttractionsScrapper( {self.attractions_urls})'


if __name__ == '__main__':
    scrapper = TripAdvisorAttractionsScrapper('path', 'url')
    scrapper.get_attractions()
