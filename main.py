import requests
from bs4 import BeautifulSoup as bs
import re
import lxml
# from urllib.request import urlopen

all_urls_n = []
tittles = []


def parse_hrefs(url_default):
    r = requests.get(url_default)
    soup = bs(r.text, "html.parser")
    hrefs = []
    for data in soup.find_all('a'):
        hrefs.append(data.get('href'))
    hrefs = hrefs[46:]
    for i in hrefs:
        all_urls_n.append(i)


def parse_url(url_default):
    r = requests.get(url_default)
    soup = bs(r.text, "html.parser")
    for title in soup.find_all('title'):
        tittles.append(title.get_text())
    a = soup.find_all('div', 'elementor-tab-content')
    for data in a:
        if data.find('p') is not None and "Каталоги ссылок" not in data.text:
            temp = data.text.lower()
            # temp = temp.replace("искать", '')
            temp = temp.replace("aliexpress", '')
            temp = temp.replace('gyverkit', '')
            temp = temp.replace(",", '')
            temp = temp.replace('.', ' ')
            temp = temp.replace('https://ali', '')
            temp = temp.replace('ski', '')

            # components = [x.strip() for x in re.findall(r'[a-zA-Z1-9,. \-]+', temp)]
            # components = list(filter(None, components))
            components = [x.strip() for x in temp]
            components = list(filter(None, components))

            # temp = re.sub(r'^https?:\/\/.*[\r\n]*', '', temp, flags=re.MULTILINE)

            # temp = temp.split()

            return components


urls_project = ['https://alexgyver.ru/projects/', 'https://alexgyver.ru/projects/page/2',
                'https://alexgyver.ru/projects/page/3', 'https://alexgyver.ru/projects/page/4',
                'https://alexgyver.ru/projects/page/5']
for url in urls_project:
    parse_hrefs(url)

all_urls = []
[all_urls.append(x) for x in all_urls_n if x not in all_urls]
all_components = []
for url in all_urls:
    all_components.append(parse_url(url))

print(tittles)
for i, data in enumerate(all_components, 0):
    print(f"Компоненты в {tittles[i]}:")
    try:
        print(', '.join(i for i in data))
    except TypeError:
        print(data)
