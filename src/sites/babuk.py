from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


class Babuk(SiteCrawler):
    actor = "Babuk"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            logging.info(f"Got content: {soup is None}")
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

                logging.info(
                    f"Found victim: {victim_name} - Published date: {published_dt}")

                victim_leak_site = self.url + victim.attrs["href"][1:]

                q = self.session.query(Victim).filter_by(
                    url=victim_leak_site, site=self.site)

                if q.count() == 0:
                    # new victim
                    v = Victim(name=victim_name, url=victim_leak_site, published=published_dt,
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
