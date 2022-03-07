from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import time
import helpers.victims as victims
import helpers.pagination as pagination


class RansomEXX(SiteCrawler):
    actor = "RansomEXX"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")
        # get max page number
        victim_list = soup.find_all("div", class_="card-body")

        for victim in victim_list:
            victim_name = victim.find("h5", class_="card-title").text.strip()
            published = victim.find("p", class_="card-text mt-3 text-secondary").text[11:21]
            published_dt = datetime.strptime(
                published, "%Y-%m-%d")
            victim_leak_site = self.url + victim.find("a", class_="btn btn-outline-primary").attrs["href"]

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()
        self.site.last_scraped = datetime.utcnow()
        # just for good measure
        self.session.commit()

        # in case server/tor proxy relay times out, slowing down scraping a bit
        time.sleep(1.0)

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p, "page-link")
