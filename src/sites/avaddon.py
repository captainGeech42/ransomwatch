from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Avaddon(SiteCrawler):
    actor = "Avaddon"
    
    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_divs = soup.find_all("div", class_="border-top border-light pt-3 mb-4")

        for div in victim_divs:
            # parse all the stuff out of the html
            name = div.find("h3").text.split("\n")[0].strip()

            url = div.find_all("div")[-1].find("a").attrs["href"]

            logging.debug(f"Found victim: {name}")

            victims.append_victims(self, url, name, None)

        self.session.commit()

    def handle_page_type(self, url: str):
        with Proxy() as p:
            r = p.get(f"{url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            page_list = soup.find("ul", class_="pagination pagination-sm justify-content-center mb-0")
            last_li = page_list.find_all("li")[-2]

            max_page_num = int(last_li.find("a").text)

            pagination.handle_pages_backwards(self, p, max_page_num)

        # just for good measure
        self.session.commit()

    def scrape_victims(self):
        # there are two types of pages
        pages = [
            f"{self.url}/",
            f"{self.url}/disclosed"
        ]

        for p in pages:
            self.handle_page_type(p)
        
        self.site.last_scraped = datetime.utcnow()
        self.session.commit()
