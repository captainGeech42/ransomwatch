from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


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
                q = self.session.query(Victim).filter_by(site=self.site, name=victim_name)

                if q.count() == 0:
                    # new victim
                    v = Victim(name=victim_name, published=None,
                               first_seen=datetime.utcnow(), last_seen=datetime.utcnow(), site=self.site)
                    self.session.add(v)
                    self.new_victims.append(v)
                else:
                    # already seen, update last_seen
                    v = q.first()
                    v.last_seen = datetime.utcnow()

                # add the org to our seen list
                self.current_victims.append(v)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
