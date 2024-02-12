import csv
import re

from urllib.parse import urljoin

import requests
import requests_cache

from bs4 import BeautifulSoup

# Enable caching to reduce network calls for previously made requests
requests_cache.install_cache('cache')

def iter_next_page(url):
    """
    Generator to iterate over pages starting from a given URL.
    Yields BeautifulSoup objects for each page with a 'Next page' link.
    """
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            break  # Exit if there's an error loading the page
        soup = BeautifulSoup(response.content, "lxml")
        yield soup
        next_link = soup.find('a', text='Следующая страница')
        url = urljoin(url, next_link.get('href')) if next_link else None

def art_list():
    """
    Generator that yields URLs of Wikipedia articles in a specific category.
    Filters out non-article links using a pre-compiled regular expression.
    """
    base_url = 'https://ru.wikipedia.org'
    start_path = '/w/index.php?title=Категория:Картины_по_алфавиту'
    full_url = urljoin(base_url, start_path)

    exlude_list = '|'.join([
        '%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:',
        '%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:',
        '%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0:',
        '%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:',
        '%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:',
        '%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0',
    ])

    exclude_pattern = re.compile(rf'^/wiki/(?!{exlude_list})')
    for soup in iter_next_page(full_url):
        for li in soup.find_all('li'):
            a = li.find('a', href=exclude_pattern)
            if a:
                yield urljoin(base_url, a.get('href'))

def main():
    """
    Main function to fetch data and save it to a CSV file.
    """
    # Open (or create) a CSV file to write the data
    with open('wikipedia_art_links.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Image URL', "Author", "Name", 'Description'])
        
        for link in art_list():
            print(link)
            w_resp = requests.get(link, stream=False)
            w_soup = BeautifulSoup(w_resp.content, "lxml")
            box = w_soup.find('table', {'class': 'infobox'})
            if box:
                data = [t.text.strip() for t in box.find_all('tr') or []]
                if len(data)>2:
                    print("---", data, "---")
                    _, author, name_ru = data[:3]
                    desc = " ".join(data[3:])
                    print(author)
                    print(name_ru)
                    print(desc)
                    img_tag = box.find('img')
                    img_url = 'https:' + img_tag['src'] if img_tag else None
                    # Write the extracted data to the CSV file
                    writer.writerow([img_url, author, name_ru, desc])
                                              

if __name__ == "__main__":
    main()
