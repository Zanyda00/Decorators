import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from tools import logger


@logger(path='log.log')
def get_headers():
    return Headers(browser="firefox", os="win").generate()


@logger(path='log.log')
def get_all_vac_links():
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers())
    soup = BeautifulSoup(response.text, 'lxml')
    vacancy_list = soup.find_all('a', class_='serp-item__title')
    all_vac_links = [i['href'] for i in vacancy_list]
    return all_vac_links


@logger(path='log.log')
def get_sort_vac_links(all_vac_links):
    sort_vac_links = []
    for link in all_vac_links:
        responce = requests.get(f'{link}', headers=get_headers())
        soup = BeautifulSoup(responce.text, 'lxml')
        description = soup.find('div', class_='vacancy-section').text.lower()
        if 'django' in description or 'flask' in description:
            sort_vac_links.append(link)
    return sort_vac_links


@logger(path='log.log')
def get_vac_inf(sort_vac_links):
    vac_inf = []
    for link in sort_vac_links:
        responce = requests.get(f'{link}', headers=get_headers())
        soup = BeautifulSoup(responce.text, 'lxml')
        salary = soup.find(class_="bloko-header-section-2 bloko-header-section-2_lite").text
        comp_name = soup.find('span', class_='vacancy-company-name').text
        try:
            city = soup.find('div', class_='vacancy-company-redesigned').find('p').text
        except AttributeError:
            city = soup.find('div', class_='vacancy-company-redesigned') \
                       .find('a', class_="bloko-link bloko-link_kind-tertiary bloko-link_disable-visited") \
                       .find('span').text.split()[0][:-1]
        vac_inf.append({
            'link': link,
            'salary': salary,
            'comp_name': comp_name,
            'city': city
        })
    return vac_inf


@logger(path='log.log')
def record_in_json(vac_inf):
    with open('vac_inf.json', 'w') as file:
        json.dump(vac_inf, file)


if __name__ == '__main__':
    all_vac_links = get_all_vac_links()
    sort_vac_links = get_sort_vac_links(all_vac_links)
    vac_inf = get_vac_inf(sort_vac_links)
    record_in_json(vac_inf)

    with open('vac_inf.json', 'r') as f:
        data = json.load(f)
    print(data)
