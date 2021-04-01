import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import urllib3
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# proxy = {"https": "localhost:8080"} this line turn on proxy
cred = credentials.Certificate(r'C:\Users\Владимир\Desktop\uirebase\key_firebase.json')
default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://parsing-ebd79-default-rtdb.firebaseio.com/'})
ref = db.reference("/")
# help("modules") - give the info about modules downloaded in pc or virtual inviromemental modules
print("Enter the city")
city = input()
print("Enter the profession")
profession = input()
print("Enter the salary in rubles")
salary = input()

base_url = "https://hh.ru"
URL = 'https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=' + quote(city) + '+' + quote(
    profession) + '&only_with_salary=true&salary=' + salary + '&from=cluster_compensation&showClusters=true'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/88.0.4324.190 Safari/537.36', 'accept': '*/*'}
print(URL)
urllib3.disable_warnings()


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, verify=False)  # proxies=proxy
    return r


def get_links(html):  # get links on the vacancy
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('span', class_='g-user-content')
    all_links = []
    for link in links:
        lim = link.find('a')
        all_links.append(lim.get('href'))
    return all_links


def get_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    salaries = soup.find_all('span', class_='bloko-section-header-3 bloko-section-header-3_lite')
    all_salaries = []
    for salwar in salaries:
        all_salaries.append(salwar.text)
    return all_salaries


def get_pages_count(html):  # get the number of pages, which will be scraping
    soup = BeautifulSoup(html, 'html.parser')
    count_page = soup.find_all('a', class_='bloko-button HH-Pager-Control')
    print(count_page)
    if count_page:
        return int(count_page[-1].get_text())
    else:
        return 1


def parse():
    pages = 0
    html = get_html(URL)
    pages_count = get_pages_count(html.text)
    info = {}
    number_of_vacancy = 1
    # Python idiom for loops like that.
    for pages in range(pages_count):
        single_link = URL + "&page=" + str(pages)
        cur_url = urljoin(base_url, single_link)
        print(cur_url)
        html = get_html(cur_url)
        links = get_links(html.text)
        content_count = len(links)
        salaries = get_info(html.text)
        print(salaries)
        for i in range(content_count):
            print(salaries[i * 2])
            print(links[i])
            print(salaries[i * 2 + 1])
            info[number_of_vacancy] = [salaries[i * 2], links[i], salaries[i * 2 + 1].replace(u'\xa0', u' ')]
            # .replace('\xa0', " ") - change symbol \xa0 in utf-8 on ' '
            number_of_vacancy = number_of_vacancy + 1
        links.clear()
        salaries.clear()

    print('End')
    return info


# parse once and then use the result.
# no need to call "parse" 3 times
info = parse()

# set the flag so it doesn't try to convert Unicode chars
s = json.dumps(info, ensure_ascii=False)
print(s)

# fn = r'C:\Users\Владимир\PycharmProjects\Parser\f.json'

# before writing to file, make sure
# - open for writing bytes
# - convert string to bytes before writing
with open('f.json', 'wb') as file_end:  # wb - write bytes
    file_end.write(bytes(s, encoding='utf-16'))
    firebase_json = ref.get()
    print(firebase_json)
    print(file_end)
    ref.delete()
    ref.update(info)
print("\U0001f637")
# vacancy-serp-item__row vacancy-serp-item__row_header
# https://ekaterinburg.hh.ru/vacancies/programmist?page=1
# https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=
# https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82
# https://hh.ru/search/vacancy?area=3&clusters=true&enable_snippets=true&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&only_with_salary=true&salary=75325&from=cluster_compensation&showClusters=true
# firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-firebase-db'})
