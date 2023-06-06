from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

CHROME_DRIVER_PATH = '/Users/segc/Documents/chromedriver/chromedriver'


class Attraction:
    def __init__(self, name: str, description: str, duration: str, location: str, city: str) -> None:
        pass

    def __str__(self) -> str:
        return f'Name: {self.name}\nDescription: {self.description}\nDuration: {self.duration}\nLocation: {self.location}\nCity: {self.city}'

urls = [
    'https://www.tripadvisor.co/Attraction_Review-g294074-d531644-Reviews-National_Museum_of_Colombia-Bogota.html'
]

attractions: list[Attraction] = []

class TripAdvisorScrapper:

    def __init__(self, path, url) -> None:
        self.driver: Chrome = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(url)

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
        attraction = Attraction(title, body, duration, location, 'Bogotá')
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

        attraction = Attraction(title, body, duration, location, 'Bogotá')
        return attraction

# for url in urls:
#     print('###################'+url+'###################')
#     scrapper = TripAdvisorScrapper(CHROME_DRIVER_PATH, url)
#     attractionScrapped = scrapper.get_site_description()
#     print(attractionScrapped)
#     attractions.append(attractionScrapped)
#     print('################### END ###################')
# print (attractions)
# # scrapper = TripAdvisorScrapper(CHROME_DRIVER_PATH)
# # scrapper.get_site_description()
