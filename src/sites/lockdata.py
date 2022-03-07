from datetime import datetime
import logging
import re
from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

import helpers.victims as victims


class LockData(SiteCrawler):
    actor = "LockData"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", {'class' : re.compile('auction-item _.*')})

            for victim in victim_list:
                victim_name = victim.find("div", class_="auction-item-info__title").text.strip()
                published_dt = None

                victim_leak_site = self.url + victim.find("div", class_="auction-item-info__title").find("a").attrs["href"]

                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
