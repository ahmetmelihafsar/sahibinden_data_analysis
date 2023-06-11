import time
import random
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import bs4
import pandas as pd

import dataclasses
from dataclasses import dataclass, field


@dataclass
class CarListing:
    brand: str
    series: str
    model: str
    ad_title: str
    year: int
    mileage: int
    color: str
    price: float
    ad_date: str
    city: str
    district: str
    url: str

    def __post_init__(self):
        for field_name in self.__dataclass_fields__:
            field_value = getattr(self, field_name)
            if field_value == dataclasses.MISSING:
                raise ValueError(f"{field_name} is required.")


def parse_row(row: bs4.Tag, by:str, brand_name:str):

    if by == 'all':
        # Extracting the data from the HTML
        marka = row.find(
            'td', class_='searchResultsTagAttributeValue').text.strip()
        seri = row.find('td', class_='searchResultsTagAttributeValue').find_next(
            'td').text.strip()
        model = row.find('td', class_='searchResultsTagAttributeValue').find_next(
            'td').find_next('td').text.strip()
    elif by== 'brand':
        marka = brand_name
        seri = row.find('td', class_='searchResultsTagAttributeValue').text.strip()
        model = row.find('td', class_='searchResultsTagAttributeValue').find_next(
            'td').text.strip()
    ilan_basligi = row.find('a', class_='classifiedTitle').text.strip()
    url = row.find('a', class_='classifiedTitle').get('href')
    yil = int(row.find('td', class_='searchResultsAttributeValue').text.strip())
    km = int(row.find('td', class_='searchResultsAttributeValue').find_next(
        'td').text.strip().replace('.', ''))
    renk = row.find('td', class_='searchResultsAttributeValue').find_next(
        'td').find_next('td').text.strip()
    fiyat = float(row.find('td', class_='searchResultsPriceValue').text.strip(
    ).split()[0].replace('.', ''))
    # ilan_tarihi = row.find('td', class_='searchResultsDateValue').find(
    #     'span').text.strip()
    ilan_tarihi = re.sub(r'\n+', ' ', row.find('td', {'class': 'searchResultsDateValue'}).text.strip()) 

    il = row.find(
        'td', class_='searchResultsLocationValue').contents[0].text.strip()
    ilce = row.find(
        'td', class_='searchResultsLocationValue').contents[2].text.strip()

    # Creating a CarListing instance
    car = CarListing(
        brand=marka,
        series=seri,
        model=model,
        ad_title=ilan_basligi,
        year=yil,
        mileage=km,
        color=renk,
        price=fiyat,
        ad_date=ilan_tarihi,
        city=il,
        district=ilce,
        url=url
    )
    return car


def scrape_cars(url: str, driver: webdriver.Chrome, by:str, brand_name:str) -> list[CarListing]:
    # Scraping the data
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    randTime = random.random() * 5
    time.sleep(5 + randTime)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find("tbody", {"class": "searchResultsRowClass"})

    # Find all the rows with the specified class
    rows_to_remove = table.find_all(
        'tr', class_='searchResultsItem nativeAd classicNativeAd')

    # Remove each row from the table
    for row in rows_to_remove:
        row: bs4.Tag
        row.extract()

    rows = table.find_all("tr", {"class": "searchResultsItem"})

    cars = []

    for row in rows:
        try:
            car = parse_row(row, by, brand_name)
        except Exception as e:
            print(row)
            raise e
        print(car)
        cars.append(car)

    return cars


brand_items = [{'name': 'Alfa Romeo',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3545&sorting=price_asc',
                'count': 24,
                'category': 3545},
               {'name': 'Audi',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3549&sorting=price_asc',
                'count': 531,
                'category': 3549},
               {'name': 'BMW',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3551&sorting=price_asc',
                'count': 995,
                'category': 3551},
               {'name': 'Chery',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=23271&sorting=price_asc',
                'count': 1,
                'category': 23271},
               {'name': 'Chevrolet',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3555&sorting=price_asc',
                'count': 73,
                'category': 3555},
               {'name': 'Chrysler',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3556&sorting=price_asc',
                'count': 7,
                'category': 3556},
               {'name': 'Citroën',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3557&sorting=price_asc',
                'count': 206,
                'category': 3557},
               {'name': 'Cupra',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=246122&sorting=price_asc',
                'count': 7,
                'category': 246122},
               {'name': 'Dacia',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3559&sorting=price_asc',
                'count': 86,
                'category': 3559},
               {'name': 'Daihatsu',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3561&sorting=price_asc',
                'count': 2,
                'category': 3561},
               {'name': 'DS Automobiles',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=233138&sorting=price_asc',
                'count': 9,
                'category': 233138},
               {'name': 'Ferrari',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3564&sorting=price_asc',
                'count': 1,
                'category': 3564},
               {'name': 'Fiat',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3607&sorting=price_asc',
                'count': 858,
                'category': 3607},
               {'name': 'Ford',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3565&sorting=price_asc',
                'count': 558,
                'category': 3565},
               {'name': 'Geely',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=90019&sorting=price_asc',
                'count': 4,
                'category': 90019},
               {'name': 'Honda',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3567&sorting=price_asc',
                'count': 436,
                'category': 3567},
               {'name': 'Hyundai',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3568&sorting=price_asc',
                'count': 482,
                'category': 3568},
               {'name': 'Infiniti',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=89919&sorting=price_asc',
                'count': 1,
                'category': 89919},
               {'name': 'Jaguar',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3571&sorting=price_asc',
                'count': 10,
                'category': 3571},
               {'name': 'Kia',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3572&sorting=price_asc',
                'count': 90,
                'category': 3572},
               {'name': 'Lada',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3573&sorting=price_asc',
                'count': 8,
                'category': 3573},
               {'name': 'Lancia',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3575&sorting=price_asc',
                'count': 3,
                'category': 3575},
               {'name': 'Lexus',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3576&sorting=price_asc',
                'count': 1,
                'category': 3576},
               {'name': 'Maserati',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3579&sorting=price_asc',
                'count': 3,
                'category': 3579},
               {'name': 'Mazda',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3580&sorting=price_asc',
                'count': 27,
                'category': 3580},
               {'name': 'Mercedes - Benz',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3581&sorting=price_asc',
                'count': 733,
                'category': 3581},
               {'name': 'MG',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=64227&sorting=price_asc',
                'count': 1,
                'category': 64227},
               {'name': 'Mini',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3584&sorting=price_asc',
                'count': 46,
                'category': 3584},
               {'name': 'Mitsubishi',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3585&sorting=price_asc',
                'count': 12,
                'category': 3585},
               {'name': 'Nissan',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3588&sorting=price_asc',
                'count': 43,
                'category': 3588},
               {'name': 'Opel',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3591&sorting=price_asc',
                'count': 750,
                'category': 3591},
               {'name': 'Peugeot',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3592&sorting=price_asc',
                'count': 412,
                'category': 3592},
               {'name': 'Porsche',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3595&sorting=price_asc',
                'count': 25,
                'category': 3595},
               {'name': 'Regal Raptor',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=250043&sorting=price_asc',
                'count': 1,
                'category': 250043},
               {'name': 'Renault',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3597&sorting=price_asc',
                'count': 1635,
                'category': 3597},
               {'name': 'RKS',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=248079&sorting=price_asc',
                'count': 1,
                'category': 248079},
               {'name': 'Rolls-Royce',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3598&sorting=price_asc',
                'count': 2,
                'category': 3598},
               {'name': 'Rover',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3599&sorting=price_asc',
                'count': 4,
                'category': 3599},
               {'name': 'Saab',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3600&sorting=price_asc',
                'count': 2,
                'category': 3600},
               {'name': 'Seat',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3601&sorting=price_asc',
                'count': 252,
                'category': 3601},
               {'name': 'Skoda',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3602&sorting=price_asc',
                'count': 258,
                'category': 3602},
               {'name': 'Smart',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3603&sorting=price_asc',
                'count': 3,
                'category': 3603},
               {'name': 'Subaru',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3604&sorting=price_asc',
                'count': 3,
                'category': 3604},
               {'name': 'Suzuki',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3605&sorting=price_asc',
                'count': 13,
                'category': 3605},
               {'name': 'Tata',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3606&sorting=price_asc',
                'count': 5,
                'category': 3606},
               {'name': 'Tesla',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=236720&sorting=price_asc',
                'count': 2,
                'category': 236720},
               {'name': 'Tofaş',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=113644&sorting=price_asc',
                'count': 237,
                'category': 113644},
               {'name': 'Toyota',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3608&sorting=price_asc',
                'count': 395,
                'category': 3608},
               {'name': 'Volkswagen',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3611&sorting=price_asc',
                'count': 1688,
                'category': 3611},
               {'name': 'Volta',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=249751&sorting=price_asc',
                'count': 2,
                'category': 249751},
               {'name': 'Volvo',
                'href': '/kategori-vitrin?viewType=Classic&pagingSize=50&category=3612&sorting=price_asc',
                'count': 83,
                'category': 3612}]
