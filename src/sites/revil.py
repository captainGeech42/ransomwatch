from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class REvil(SiteCrawler):
    actor = "REvil"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_divs = soup.find_all("div", class_="blog-post-container")

        for div in victim_divs:
            # parse all the stuff out of the html
            parent_div = div.find("div")
            child_div = parent_div.find("div")

            title_link = child_div.find("h2").find("a")
            name = title_link.text.strip()

            url = self.url + title_link.attrs["href"]

            logging.debug(f"Found victim: {name}")

            victims.append_victims(self, url, name, None)

        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            page_list = soup.find("ul", class_="pagination")
            last_li = page_list.find_all("li")[-2]

            max_page_num = int(last_li.find("a").text)

            pagination.handle_pages_backwards(self, p, max_page_num)

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
