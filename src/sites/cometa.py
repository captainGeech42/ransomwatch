from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.pagination as pagination
import helpers.victims as victims


class Cometa(SiteCrawler):
    actor = "ElCometa"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("div", class_="card-body")

        for victim in victim_list:
            victim_name = victim.find("h5", class_="card-title").text.strip()

            victim_leak_site = self.url + victim.find("div", class_="col-sm-2 browse-files-b").find("a").attrs["href"]
            published_dt = datetime.now()

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p)
