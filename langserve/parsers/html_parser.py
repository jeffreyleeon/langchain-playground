from urllib.request import urlopen
from bs4 import BeautifulSoup

class USCISParser:

    def __init__(self):
        self.base_url = 'https://www.uscis.gov'
        self.url = f'{self.base_url}/working-in-the-united-states'
        self.menu_class = 'menu--main'

    def parse_urls_in_page(self):
        page = urlopen(self.url).read()
        soup = BeautifulSoup(page)
        soup.prettify()
        menu = soup.find("ul", {"class": self.menu_class})
        hyperlinks = menu.find_all("a", href=True)
        urls = []
        for hyperlink in hyperlinks:
            href = hyperlink['href']
            if href == '#':
                continue
            # print(f"Found url: {href}")
            urls.append(f"{self.base_url}/{href}")
        return urls
