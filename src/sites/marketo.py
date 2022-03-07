from datetime import datetime
import logging
from bs4 import BeautifulSoup, NavigableString
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


def get_text(victim_name_div):
    return ''.join(victim_name_div.find_all(text=True, recursive=False)).strip()


class Marketo(SiteCrawler):
    actor = "Marketo"

    def handle_page(self, body: str):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="lot-card row m-0")

            for victim in victim_list:
                victim_name_div = victim.find("div", class_="text-left text-grey d-block overflow-hidden")
                victim_name = get_text(victim_name_div).strip().split("|")[0]

                published_dt = None

                victim_leak_site = victim.find(
                    "div", class_="text-left text-grey d-block overflow-hidden"
                ).find("a").attrs["href"]

                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p, "page-item")
