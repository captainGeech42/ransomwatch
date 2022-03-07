import logging
import re
from datetime import datetime
from bs4 import BeautifulSoup
import dateparser
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination

class Arvin(SiteCrawler):
    actor = "Arvin"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")
        victim_list = soup.find_all("article", {"id": re.compile("post.*")})

        for victim in victim_list:
            victim_name = victim.find("h2", class_="type-list-title").text.strip()
            victim_leak_site = victim.find("h2", class_="type-list-title").find("a").attrs["href"]

            published = victim.find("div", class_="type-list-date").text.strip()

            published_dt = dateparser.parse(published)
            if published_dt is None and len(published) > 0:
                logging.warning(f"couldn't parse timestamp: {published}")

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p)
