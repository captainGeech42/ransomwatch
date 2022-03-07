import logging
from datetime import datetime
from bs4 import BeautifulSoup
import dateparser
from dateutil.relativedelta import relativedelta
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims

class Pysa(SiteCrawler):
    actor = "Pysa"

    def scrape_victims(self):
        with Proxy() as p:
            url = self.url + '/partners.html'
            r = p.get(f"{url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="page-header")

            for victim in victim_list:
                victim_name = victim.find_all("a")[0].text.strip()
                published = victim.find_all("span")[1].text.strip()

                # they use a bunch of different date format
                # use a nice dateparsing library to handle them all in an easier manner
                published_dt = dateparser.parse(published)
                # sometimes they don't have a timestamp
                if published_dt is None and len(published) > 0:
                    logging.warning(f"couldn't parse timestamp: {published}")

                victim_leak_site = self.url + '/' + victim.find_all("a")[0].attrs["href"]
                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
