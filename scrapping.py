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
        self.title = title
        self.description = description
        self.duration = duration
        self.location = location
        self.city = city


    def __str__(self) -> str:
        return f'Name: {self.title}\nDescription: {self.description}\nDuration: {self.duration}\nLocation: {self.location}\nCity: {self.city}'

class TripAdvisorAttractionScrapper:

    def __init__(self, path, url) -> None:
        self.driver: Chrome = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(url)

    def get_site_description(self):
        try:
            attraction = self.get_site_attractions_strategy_1()
        except Exception as e:
            try:
                print('Strategy 1 failed')
                print(e)
                attraction = self.get_site_attractions_strategy_2()
            except Exception as e:
                print('Strategy 2 failed')
                print(e)
        return attraction

    def get_site_attractions_strategy_1(self):
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
        attraction = Attraction(title.text, body.text, duration.text, location.text, 'Bogotá')
        return attraction

    def get_site_attractions_strategy_2(self):
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

        attraction = Attraction(title.text, body.text, duration.text, location.text, 'Bogotá')
        return attraction
    
class TripAdvisorAttractionLoader:

    def load_site_attractions_data(self, city_name):
        if city_name not in ('Atlantico', 'Bogota', 'Boyaca', 'Bucaramanga', 'Cartagena', 'Medellin', 'SantaMarta', 'ValleDelCauca'):
            print('La ciudad no es valida')
            return
        
        df = pd.read_csv(f'attractions_{city_name}.csv')
        df['title']  = ''
        df['description'] = ''
        df['duration'] = ''
        df['location'] = ''
        df['city'] = ''

        for i in range(len(df)):
            try:
                scrapper = TripAdvisorAttractionScrapper('path', df['url'][i])
                attractionScrapped = scrapper.get_site_description()
                df['title'][i]  = attractionScrapped.title
                df['description'][i]  = attractionScrapped.description
                df['duration'][i]  = attractionScrapped.duration
                df['location'][i]  = attractionScrapped.location
                df['city'][i]  = attractionScrapped.city
            except:
                continue
        df.to_csv(f'attractions_{city_name}.csv')

if __name__ == '__main__':
    scrapper = TripAdvisorAttractionLoader()
    scrapper.load_site_attractions_data('Bogota')