from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class Pay2Key(SiteCrawler):
    actor = "Pay2Key"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="article")

            for victim in victim_list:
                victim_name = victim.find("h3").find("a").text.strip()

                victim_leak_site = self.url + victim.find("a").attrs["href"][1:]  # they have a dot before the link

                victims.append_victims(self, victim_leak_site, victim_name, None)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
