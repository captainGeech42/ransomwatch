from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Conti(SiteCrawler):
    actor = "Conti"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_divs = soup.find_all("div", class_="card")

        for div in victim_divs:
            # parse all the stuff out of the html
            name = div.find("div", class_="title").text[1:-1].strip()

            footer_div = div.find("div", class_="footer")
            published = footer_div.find("div")
            published_dt = datetime.strptime(published.text.strip(), "%B %d, %Y")

            url = self.url + footer_div.find_all("div")[-1].find("a").attrs["href"]

            logging.debug(f"Found victim: {name}")

            victims.append_victims(self, url, name, published_dt)

        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            page_list = soup.find("ul", class_="pages")
            last_li = page_list.find_all("li")[-1]

            max_page_num = int(last_li.find("a").attrs["href"].split("/")[2])

            pagination.handle_pages_backwards(self, p, max_page_num)

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
