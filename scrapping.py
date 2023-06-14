from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import random
import time


class Attraction:
    def __init__(self, title: str, description: str, duration: str, location: str, city: str):
        try:
            if title:
                print(f'Title is valid {title}')
                self.title = title.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
                print(self.title)
            else:
                self.title = None
            if description:
                print(f'Description is valid {description}')
                self.description = description.replace(
                    '"', '').replace(',', '').replace('\n', '').strip()
                print(self.description)
            else:
                self.description = None
            if duration:
                print(f'Duration is valid {duration}')
                self.duration = duration.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
                print(self.duration)
            else:
                self.duration = None
            if location:
                print(f'Location is valid {location}')
                self.location = location.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
                print(self.location)
            else:
                self.location = None
            if city:
                print(f'City is valid {city}')
                self.city = city.replace('"', '').replace(
                    ',', '').replace('\n', '').strip()
                print(self.city)
            else:
                self.city = None
        except Exception as e:
            print(e)

    def __str__(self) -> str:
        return f'Name: {self.title}\nDescription: {self.description}\nDuration: {self.duration}\nLocation: {self.location}\nCity: {self.city}'


class TripAdvisorAttractionScrapper:
    def __init__(self,  driver) -> None:
        self.driver: Chrome = driver

    def get_site_description(self, city_name, url):
        print('\n\n\n')
        print('######### STARTING GETTING ATTRACTION #########')
        print(f'City: {city_name}')
        print(f'Url: {url}')
        self.url = url
        self.driver.get(url)
        time.sleep(random.uniform(0, 2))
        try:
            attraction = self.get_site_attractions(city_name)
            if not attraction:
                raise Exception('Attraction not found')
            return attraction
        except Exception as e:
            print('####### UNKNOW ERROR #########')
            print(e)
            return None

    def get_site_title(self) -> str:
        print('#### Called get_site_title ####')
        time.sleep(random.uniform(0, 1))
        try:
            print('#### Waiting for title ####')
            WebDriverWait(self.driver, 5).until(lambda x: x.find_element(
                By.XPATH,
                '/html/body/div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1',
            ))
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.refresh()
        try:
            print('#### Trying to get title ####')
            return self.driver.find_element(
                By.XPATH,
                '/html/body/div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1'
            ).text
        except Exception as e:
            print(f'Title not found for attraction {self.url}')
            print(e)
            return None

    def get_site_duration(self):
        print('#### Called get_site_duration ####')
        time.sleep(random.uniform(0, 1))
        try:
            return self.driver.find_element(
                By.XPATH,
                '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[3]/div[2]'
            ).text
        except Exception as e:
            print(f'Duration not found for attraction {self.url}')
            print(e)
            return None

    def get_site_location(self):
        print('#### Called get_site_location ####')
        time.sleep(random.uniform(0, 1))
        try:
            return self.driver.find_element(
                By.XPATH,
                '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[5]/div/div/div[2]/div[1]/div/div/div/div[1]/button/span',
            ).text
        except Exception as e:
            print(f'Location not found for attraction {self.url}')
            print(e)
            return None

    def get_site_body(self):
        print('#### Called get_site_body ####')
        time.sleep(random.uniform(0, 1))
        try:
            return self.driver.find_element(
                By.XPATH,
                '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div',
            ).text
        except Exception as e:
            print(f'Description not found for attraction {self.url}')
            print(e)
            return None

    def get_site_attractions(self, city_name):
        print('#### Called get_site_attractions ####')
        time.sleep(random.uniform(0, 1))
        return Attraction(
            city=city_name,
            title=self.get_site_title(),
            description=self.get_site_body(),
            duration=self.get_site_duration(),
            location=self.get_site_location(),
        )


class TripAdvisorAttractionLoader:

    def load_site_attractions_data(self, city_name):
        df = pd.read_csv(f'attractions_{city_name}.csv')
        df['title'] = ''
        df['description'] = ''
        df['duration'] = ''
        df['location'] = ''
        # df['city'] = ''

        driver = webdriver.Chrome(ChromeDriverManager().install())

        for i in range(len(df)):
            try:
                scrapper = TripAdvisorAttractionScrapper(driver)
                attractionScrapped = scrapper.get_site_description(
                    city_name, df['url'][i]
                )
                if attractionScrapped.title:
                    df['title'][i] = attractionScrapped.title
                if attractionScrapped.description is not None:
                    df['description'][i] = attractionScrapped.description
                if attractionScrapped.duration:
                    df['duration'][i] = attractionScrapped.duration
                if attractionScrapped.location:
                    df['location'][i] = attractionScrapped.location
                # if attractionScrapped.city:
                #     df['city'][i] = attractionScrapped.city
            except Exception as e:
                print('######## Start error #########')
                print(f'Error in {df["url"][i]}')
                print(e)
                print('######## End error #########')
                pass
        df.to_csv(f'attractions_{city_name}_populated_v2.csv', index=False)


if __name__ == '__main__':
    # for i in ['Atlantico', 'Bogota', 'Boyaca', 'Bucaramanga', 'Cartagena', 'Medellin', 'SantaMarta', 'ValleDelCauca']:
    scrapper = TripAdvisorAttractionLoader()
    scrapper.load_site_attractions_data('Medellin')
    # time.sleep(random.uniform(30, 60))
