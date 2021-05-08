from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


class Cl0p(SiteCrawler):
    actor = "Cl0p"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find("div", class_="collapse-section").find_all("li")
            for victim in victim_list:
                victim_name = victim.find("a").text.strip()
                
                if victim_name == "HOME" or victim_name == "HOW TO DOWNLOAD?":
                    continue
                
                
                victim_leak_site = self.url + victim.find("a").attrs["href"]
                
                
                q = self.session.query(Victim).filter_by(
                    url=victim_leak_site, site=self.site)

                if q.count() == 0:
                    # new victim
                    v = Victim(name=victim_name, url=victim_leak_site, published=None,
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
