from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class Cl0p(SiteCrawler):
    actor = "Cl0p"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find("ul", class_="g-toplevel").find_all("li", class_="g-menu-item")
            for victim in victim_list:
                victim_name = victim.find("span", class_="g-menu-item-title").text.strip()

                if victim_name in ("HOME", "HOW TO DOWNLOAD?", "ARCHIVE"):
                    continue

                victim_leak_site = self.url + victim.find("a").attrs["href"]

                victims.append_victims(self, victim_leak_site, victim_name, None)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
