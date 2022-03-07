from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Ragnarok(SiteCrawler):
    actor = "Ragnarok"

    def handle_page(self, body: str):

        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("div", class_="post-entry")

        for victim in victim_list:
            victim_name = victim.find("div", class_="post-title").text.strip()

            published = victim.find("div", class_="post-time")
            published_dt = datetime.strptime(
                published.text.strip(), "%Y-%m-%d")

            victim_leak_site = self.url + victim.find("div", class_="post-title").find("a").attrs["href"]

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p, "page-number")
