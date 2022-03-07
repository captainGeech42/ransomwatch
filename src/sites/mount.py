from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class Mount(SiteCrawler):
    actor = "Mount"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="blog-one__single")

            for victim in victim_list:
                victim_name = victim.find("h3").text.strip()

                client_site = victim.find("h3").find("a", title="Visit Client Website").text.strip()
                victim_name = victim_name.replace(client_site, "").strip()

                published = victim.find("div", class_="blog-one__meta").text.strip()[:10]

                published_dt = datetime.strptime(
                    published, "%Y-%m-%d")

                victim_leak_site = self.url + "/" + victim.find("h3").find("a").attrs["href"]

                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
