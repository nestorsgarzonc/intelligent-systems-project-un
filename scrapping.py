from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

CHROME_DRIVER_PATH = '/Users/segc/Documents/chromedriver/chromedriver'

urls = [
    'https://www.tripadvisor.co/Attraction_Review-g294074-d531644-Reviews-National_Museum_of_Colombia-Bogota.html'
]


class Attraction:
    def __init__(self, title: str, description: str, duration: str, location: str, city: str):
        try:
            if (title):
                self.title = title.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
            if (description):
                self.description = description.replace(
                    '"', '').replace(',', '').replace('\n', '').strip()
            if (duration):
                self.duration = duration.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
            if (location):
                self.location = location.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
            if (city):
                self.city = city.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
        except Exception as e:
            print(e)

    def __str__(self) -> str:
        return f'Name: {self.title}\nDescription: {self.description}\nDuration: {self.duration}\nLocation: {self.location}\nCity: {self.city}'


class TripAdvisorAttractionScrapper:

    def __init__(self, url, driver) -> None:
        self.driver: Chrome = driver
        self.driver.get(url)

    def get_site_description(self, city_name):
        try:
            attraction = self.get_site_attractions_strategy_1(city_name)
            if not attraction:
                raise Exception('Attraction not found')
            return attraction
        except Exception as e:
            try:
                print('Strategy 1 failed')
                print(e)
                attraction = self.get_site_attractions_strategy_2(city_name)
                if not attraction:
                    raise Exception('Attraction not found')
                return attraction
            except Exception as e:
                print('Strategy 2 failed')
                print(e)

    def get_site_attractions_strategy_1(self, city_name):
        title = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1'
        )
        print(title.text)
        duration = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[3]/div[2]'
        )
        print(duration.text)
        location = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[5]/div/div/div[2]/div[1]/div/div/div/div[1]/button/span'
        )
        print(location.text)
        body = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div'
        )
        print(body.text)
        attraction = Attraction(title.text, body.text,
                                duration.text, location.text, city_name)
        return attraction

    def get_site_attractions_strategy_2(self, city_name):
        title = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1'
        )
        print(title.text)
        duration = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[3]/div[2]'
        )
        print(duration.text)
        location = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[5]/div/div/div[2]/div[1]/div/div/div/div[1]/button/span'
        )
        print(location.text)
        body = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div')
        print(body.text)

        attraction = Attraction(title.text, body.text,
                                duration.text, location.text, city_name)
        return attraction


class TripAdvisorAttractionLoader:

    def load_site_attractions_data(self, city_name):
        if city_name not in ('Atlantico', 'Bogota', 'Boyaca', 'Bucaramanga', 'Cartagena', 'Medellin', 'SantaMarta', 'ValleDelCauca'):
            print('La ciudad no es valida')
            return

        df = pd.read_csv(f'attractions_{city_name}.csv')
        df['title'] = ''
        df['description'] = ''
        df['duration'] = ''
        df['location'] = ''
        df['city'] = ''

        driver = webdriver.Chrome(ChromeDriverManager().install())

        for i in range(len(df)):
            try:
                scrapper = TripAdvisorAttractionScrapper(df['url'][i], driver)
                attractionScrapped = scrapper.get_site_description(city_name)
                df['title'][i] = attractionScrapped.title
                df['description'][i] = attractionScrapped.description
                df['duration'][i] = attractionScrapped.duration
                df['location'][i] = attractionScrapped.location
                df['city'][i] = attractionScrapped.city
            except Exception as e:
                print('######## Start error #########')
                print(f'Error in {df["url"][i]}')
                print(e)
                print('######## End error #########')
                continue
        df.to_csv(f'attractions_{city_name}_populated.csv')


if __name__ == '__main__':
    scrapper = TripAdvisorAttractionLoader()
    scrapper.load_site_attractions_data('Bogota')
