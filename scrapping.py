from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time

CHROME_DRIVER_PATH = '/Users/segc/Documents/chromedriver/chromedriver'


class Attraction:
    def __init__(self, name: str, description: str, duration: str, location: str, city: str) -> None:
        pass

    def __str__(self) -> str:
        return f'Name: {self.name}\nDescription: {self.description}\nDuration: {self.duration}\nLocation: {self.location}\nCity: {self.city}'


attractions: list[Attraction] = []


class TripAdvisorScrapper:
    url = 'https://www.tripadvisor.co/Attraction_Review-g294074-d531644-Reviews-National_Museum_of_Colombia-Bogota.html'

    def __init__(self, path) -> None:
        self.driver: Chrome = webdriver.Chrome()
        self.driver.get(self.url)

    def get_site_description(self):
        try:
            self.get_site_attractions_strategy_1()
        except Exception as e:
            try:
                print('Strategy 1 failed')
                print(e)
                self.get_site_attractions_strategy_2()
            except Exception as e:
                print('Strategy 2 failed')
                print(e)

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


scrapper = TripAdvisorScrapper(CHROME_DRIVER_PATH)
scrapper.get_site_description()
