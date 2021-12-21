from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import time


class RansomEXX(SiteCrawler):
    actor = "RansomEXX"

    def _handle_page(self, soup):
        victim_list = soup.find_all("div", class_="card-body")

        for victim in victim_list:
            victim_name = victim.find("h5", class_="card-title").text.strip()

            published = victim.find("p", class_="card-text mt-3 text-secondary").text[11:21]
            published_dt = datetime.strptime(
                published, "%Y-%m-%d")

            victim_leak_site = self.url + victim.find("a", class_="btn btn-outline-primary").attrs["href"]

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

        # in case server/tor proxy relay times out, slowing down scraping a bit
        time.sleep(1.0)

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get the number of pages on the site            
            page_nav = soup.find("ul", class_="pagination")
            num_pages = max([int(x.text) for x in page_nav.findAll("a")])

            for pg_num in range(1,num_pages+1):
                # scrape each page
                r = p.get(f"{self.url}/?page={pg_num}", headers=self.headers)
                soup = BeautifulSoup(r.content.decode(), "html.parser")
                self._handle_page(soup)