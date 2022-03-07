from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class Ranzy(SiteCrawler):
    actor = "Ranzy"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="col py-3")

            for victim in victim_list:
                victim_name = victim.find("h3", class_="mb-3").text.strip()

                # it's less than ideal that there aren't other properties to search on
                # but I don't want to store leak data URLs
                victims.append_victims(self, None, victim_name, None)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
