from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class Babuk(SiteCrawler):
    actor = "Babuk"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("a", class_="leak-card p-3")

            for victim in victim_list:
                victim_name = victim.find("h5").text.strip()

                published = victim.find("div", class_="col-auto published")
                published_dt = datetime.strptime(
                    published.text.strip(), "%Y-%m-%d %H:%M:%S")

                if victim_name == "Hello world 1" or victim_name == "Mercy, journalists,chonky boi":
                    # skipping news and updates
                    continue

                victim_leak_site = self.url + victim.attrs["href"]

                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
