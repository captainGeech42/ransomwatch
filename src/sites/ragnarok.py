from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


class Ragnarok(SiteCrawler):
    actor = "Ragnarok"

    def _handle_page(self, body: str):
        
        soup = BeautifulSoup(body, "html.parser")
        
        victim_list = soup.find_all("div", class_="post-entry")
        
        for victim in victim_list:
            victim_name = victim.find("div", class_="post-title").text.strip()
            
            published = victim.find("div", class_="post-time")
            published_dt = datetime.strptime(
                published.text.strip(), "%Y-%m-%d")
            
            victim_leak_site = self.url + victim.find("div", class_="post-title").find("a").attrs["href"]
            
            
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
    
    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)
            soup = BeautifulSoup(r.content.decode(), "html.parser")
            
            # find all pages
            page_nav = soup.find_all("a", class_="page-number")
            
            site_list = []
            site_list.append(self.url)
            
            for page in page_nav:
                site_list.append(self.url + page.attrs["href"])
            
            # handle each page
            for site in site_list:
                r = p.get(site, headers=self.headers)
                self._handle_page(r.content.decode())