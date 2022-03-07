from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Everest(SiteCrawler):
    actor = "Everest"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("header", class_="entry-header has-text-align-center")

        for victim in victim_list:
            victim_name = victim.find("h2", class_="entry-title heading-size-1").text.strip()

            victim_leak_site = victim.find("h2", class_="entry-title heading-size-1").find("a").attrs["href"]

            published = victim.find("li", class_="post-date meta-wrapper").find("a").text.strip()
            published_dt = datetime.strptime(
                published, "%B %d, %Y")

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p)
