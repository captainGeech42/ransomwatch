from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class LV(SiteCrawler):
    actor = "LV"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="blog-post blog-main posts_at_first")

            for victim in victim_list:
                print(victim)
                victim_name = victim.find("h2", class_="blog-post-title").find("a").text.strip()

                victim_leak_site = self.url + victim.find("h2", class_="blog-post-title").find("a").attr["href"]

                victims.append_victims(self, victim_leak_site, victim_name, None)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
