from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import time
import dateparser
import helpers.victims as victims
import helpers.pagination as pagination


class Snatch(SiteCrawler):
    actor = "Snatch"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")
        victim_list = soup.find_all("div", class_="ann-block")
        for victim in victim_list:
            victim_name = victim.find("div", class_="a-b-n-name").text.strip()
            published = victim.find("div", class_="a-b-h-time").text.strip()
            published_dt = dateparser.parse(published)
            victim_onclick = victim.find("button", class_="a-b-b-r-l-button")['onclick']
            start = victim_onclick.find("window.location='") + len("window.location='")
            victim_leak_site = self.url + victim_onclick[start:-1]
            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()
        # Lets delay execution of next in case of timeout of server/proxy relay
        time.sleep(1.0)

    def scrape_victims(self):
        with Proxy() as p:
            try:
                pagination.handle_pages_for(self, p, "m-n-n-number")
            except AttributeError:
                r = p.get(f"{self.url}", headers=self.headers)
                self.handle_page(r.content.decode())
