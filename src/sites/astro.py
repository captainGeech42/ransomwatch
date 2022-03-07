from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims

class Astro(SiteCrawler):
    actor = "Astro"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="col p-4 d-flex flex-column position-static")

            for victim in victim_list:
                victim_name = victim.find("h3", class_="mb-0").text.strip()
                victim_name = victim_name[:victim_name.find("\n")]
                

                published = victim.find("div", class_="mb-1 text-muted")
                published_dt = datetime.strptime(
                    published.text.strip(), "%Y-%m-%d")

                victim_leak_site = self.url + victim.find("a", class_="stretched-link").attrs["href"]

                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
