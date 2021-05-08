from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import time

class Nefilim(SiteCrawler):
    actor = "Nefilim"

    
    def _handle_page(self, soup):
        victim_list = soup.find_all("header", class_="entry-header")
        for victim in victim_list:
            victim_title = victim.find("h2", class_="entry-title").text.strip()
            
            victim_name = victim_title[0:victim_title.find(". Part")]
            
            meta = victim.find("div", class_="entry-meta")
            
            published = meta.find("time", class_="entry-date").attrs["datetime"]
            published_dt = datetime.strptime(
                published.strip()[:-6], "%Y-%m-%dT%H:%M:%S")
            
            victim_leak_site = meta.find("span", class_="posted-on").find("a").attrs["href"]
        
            
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
            self.current_victims.append(v)
        self.session.commit()
        
        # server was timing out so slows it down a bit
        time.sleep(1.0)
        
    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            page_count = 0
            while True:
                page_nav = soup.find("div", class_="nav-previous")
                if page_nav is None:
                    break
                
                url = page_nav.find("a").attrs["href"]
                r = p.get(f"{url}", headers=self.headers)
                soup = BeautifulSoup(r.content.decode(), "html.parser")
                self._handle_page(soup)