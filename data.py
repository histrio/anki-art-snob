import re

import requests
import requests_cache

from bs4 import BeautifulSoup, NavigableString


requests_cache.install_cache('cache')


def iter_next_page(url):
    w_resp = requests.get('https://ru.wikipedia.org/' + url, stream=False)
    w_soup = BeautifulSoup(w_resp.content, "lxml")
    yield w_soup
    next_url = w_soup.find('a', text='Следующая страница')
    if next_url:
        yield from iter_next_page(next_url.get('href'))

def art_list():
    URL = '/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
    RE = re.compile(r'^/wiki/(?!%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:|%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:|%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0:|%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:|%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:|%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0)')
    for soup in iter_next_page(URL):
        for li in soup.find_all('li'):
            a = li.find('a', href=RE)
            if a:
                yield 'https://ru.wikipedia.org/' + a.get('href')


def main():
    for link in art_list():
        print(link)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
