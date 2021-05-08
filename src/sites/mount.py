from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


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
