import logging
import validators
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)

def check_url(url):
    if validators.url(url):
        return True
    return False

class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.titles = []

    def download_url(self, url):
        return requests.get(url).text

    def get_titles(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        path = soup.title.string
        return path

    def crawl(self, url):
        html = self.download_url(url)
        return self.get_titles(url, html)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                title = self.crawl(url)
                self.titles.append(f'{title} -> {url}\n')
            except Exception:
                self.titles.append(f'no title -> {url}\n')
                logging.info(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
        return self.titles


if __name__ == '__main__':
    urls = []
    while True:
        url = input("Input url: ")
        validate_url = check_url(url)
        if validate_url:
            urls.append(url)
        else:
            print('Please enter correct url')
        next_option = int(input('If you want add other url choose 1 else 0: '))

        if next_option == 0:
            break
    titles = Crawler(urls=urls).run()
    formatted_numbers = ''
    with open('titles.txt', 'w', newline='') as myfile:
        for title in titles:
            myfile.writelines(title)
