from datetime import datetime
from bs4 import BeautifulSoup
import logging
import requests

from config import Config
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

class Avoslocker(SiteCrawler):
    actor = "Avoslocker"

    def __init__(self, url: str):
        super(Avoslocker, self).__init__(url)

        self.headers["Accept"] = "text/plain, */*"
        self.headers["Origin"] = "null"

    def is_site_up(self) -> bool:
        # can't use the parent class is_site_up() because the / route doesn't exist on the API server
        with Proxy() as p:
            try:
                r = p.get(f"{self.url}/rss", headers=self.headers, timeout=Config["timeout"])

                if r.status_code >= 400:
                    return False
            except Exception as e:
                print(e)
                return False

        self.site.last_up = datetime.utcnow()

        return True

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}/rss", headers=self.headers)

            soup = BeautifulSoup(r.content, features="xml")
            items = soup.findAll('item')

            for item in items:
                name = item.title.text

                logging.debug(f"Found victim: {name}")

                publish_dt = datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %Z")

                q = self.session.query(Victim).filter_by(site=self.site, name=name)

                if q.count() == 0:
                    # new victim
                    v = Victim(name=name, url=None, published=publish_dt, first_seen=datetime.utcnow(), last_see$
                    self.session.add(v)
                    self.new_victims.append(v)
                else:
                    # already seen, update last_seen
                    v = q.first()
                    v.last_seen = datetime.utcnow()

                # add the org to our seen list
                self.current_victims.append(v)

        self.site.last_scraped = datetime.utcnow()
        self.session.commit()
