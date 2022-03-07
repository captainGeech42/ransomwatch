from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Xing(SiteCrawler):
    actor = "Xing"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("div", class_="col p-4 d-flex flex-column position-static")

        for victim in victim_list:
            victim_name = victim.find("h3", class_="mb-0").text.strip()
            victim_name = victim_name[:victim_name.find("\n")]

            victim_leak_site = self.url + victim.find("a").attrs["href"]

            published = victim.find("div", class_="mb-1 text-muted").text.strip()
            published_dt = datetime.strptime(
                published, "%Y-%m-%d")
            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p)
