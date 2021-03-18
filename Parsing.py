import requests
import lxml
from bs4 import BeautifulSoup
from urllib.parse import quote

print("Enter the city")
city = input()
print("Enter the profession")
profeccion = input()
URL = 'https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=' + quote(city) + '+' + quote(
    profeccion)
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/88.0.4324.190 Safari/537.36', 'accept': '*/*'}

print(URL)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancy-serp-item__row vacancy-serp-item__row_header')
    links = soup.find_all('a', class_='bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy')
    # print(items)
    print(links)
    number_of_link = 0
    for item in items:
        cur_vacancy = item.find('div', class_='vacancy-serp-item__info')
        print(cur_vacancy.text)
        print(links[number_of_link].get('href'))
        number_of_link = number_of_link + 1


def parse():
    pages = 1
    html = get_html(URL)
    print(html)
    get_content(html.text)
    while pages != 2:
        soup = BeautifulSoup(html.text, 'lxml')
        linking = soup.find_all(class_='bloko-button HH-Pager-Controls-Next HH-Pager-Control')
        print(linking[0])
        single_link = linking[0].get("href")
        html = get_html(single_link)
        print(html)
        get_content(html.text)
        pages = pages + 1
    else:
        print('End')


parse()

# vacancy-serp-item__row vacancy-serp-item__row_header
# https://ekaterinburg.hh.ru/vacancies/programmist?page=1
# bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy
# https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=
# https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82
