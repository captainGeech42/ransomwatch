from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import time
import dateparser


class Rook(SiteCrawler):
    actor = "Rook"

    def _handle_page(self, soup):
        victim_list = soup.find_all("a", class_="post")
        for victim in victim_list:
            victim_name = victim.find("h2", class_="post-title").text.strip()
            published = victim.find("div", class_="time").text.strip()
            published_dt = dateparser.parse(published)
            victim_leak_site = victim['href']

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

        # Lets delay execution of next in case of timeout of server/proxy relay
        time.sleep(1.0)

    def scrape_victims(self):
        with Proxy() as p:
            # there is a pagination-container div right now but nothing in it
            # once there are multiple pages of victims, this can be updated to
            # support that

            r = p.get(f"{self.url}" + '/archives/', headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")
            self._handle_page(soup)
