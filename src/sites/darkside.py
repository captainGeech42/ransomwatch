from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

class DarkSide(SiteCrawler):
    actor = "DarkSide"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            victim_divs = soup.find("div", class_="row mt-3 mb-3").find_all("div", recursive=False)

            for div in victim_divs:
                # parse all the stuff out of the html
                parent_div = div.find("div")
                header_div = parent_div.find("div", class_="header")

                # get the name from the header
                h5 = header_div.find("div").find("div", class_="col-8").find("h5")
                name = h5.text.split("- ")[0].strip()

                # get the published date from the header
                published_span = header_div.find("div").find("div", class_="col-4 text-right").find("span")
                published_dt = datetime.strptime(published_span.text.strip(), "%d.%m.%Y")

                # parse out the details link
                # this is ugly but it works
                body_div = parent_div.find("div", class_="body")
                link_div = body_div.find_all("div")[-1]
                a = body_div.find_all("div")
                b = a[-1]
                c = b.find("a")
                url = c.attrs["href"]

                logging.debug(f"Found victim: {name}")

                # check if the org is already seen (search by url because name isn't guarenteed unique)
                q = self.session.query(Victim).filter_by(url=url, site=self.site)

                if q.count() == 0:
                    # new org
                    v = Victim(name=name, url=url, published=published_dt, first_seen=datetime.utcnow(), last_seen=datetime.utcnow(), site=self.site)
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