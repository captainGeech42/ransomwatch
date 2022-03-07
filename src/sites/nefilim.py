from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import time
import helpers.victims as victims
import helpers.pagination as pagination


class Nefilim(SiteCrawler):
    actor = "Nefilim"

    def handle_page(self, soup):
        victim_list = soup.find_all("header", class_="entry-header")
        for victim in victim_list:
            victim_title = victim.find("h2", class_="entry-title").text.strip()

            victim_name = victim_title[0:victim_title.find(". Part")]

            meta = victim.find("div", class_="entry-meta")

            published = meta.find("time", class_="entry-date").attrs["datetime"]
            published_dt = datetime.strptime(
                published.strip()[:-6], "%Y-%m-%dT%H:%M:%S")

            victim_leak_site = meta.find("span", class_="posted-on").find("a").attrs["href"]

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

        # server was timing out so slows it down a bit
        time.sleep(1.0)

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)
            soup = BeautifulSoup(r.content.decode(), "html.parser")

            pagination.handle_pages_while(self, "nav-previous", soup, p)
