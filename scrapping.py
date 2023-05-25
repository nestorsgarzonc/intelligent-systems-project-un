import time
import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
}


class Attraction:
    def __init__(self, name: str, description: str, duration: str, location: str, city: str) -> None:
        pass


attractions: list[Attraction] = []


class TripAdvisorScrapper:
    url = 'https://www.tripadvisor.co/Attraction_Review-g294074-d532215-Reviews-Museo_Botero_del_Banco_de_la_Republica-Bogota.html'

    def __init__(self) -> None:
        self.page = requests.get(self.url, headers=headers)
        self.soup: BeautifulSoup = BeautifulSoup(
            self.page.content, 'html.parser'
        )
        print(self.soup)
        self.dom = etree.HTML(str(self.soup))

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
        title = self.dom.xpath(
            '/html/body/div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1')
        print(title[0].text)
        body = self.dom.xpath(
            '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div')
        print(body[0].text)

    def get_site_attractions_strategy_2(self):
        title = self.dom.xpath(
            '/html/body/div[1]')
        print(title)
        # body = self.dom.xpath(
        #    '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div')
        # print(body[0].text)


scrapper = TripAdvisorScrapper()
time.sleep(1)
scrapper.get_site_description()
