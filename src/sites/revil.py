from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

class REvil(SiteCrawler):
    actor = "REvil"
    
    def _handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_divs = soup.find_all("div", class_="blog-post-container")

        for div in victim_divs:
            # parse all the stuff out of the html
            parent_div = div.find("div")
            child_div = parent_div.find("div")

            title_link = child_div.find("h2").find("a")
            name = title_link.text.strip()

            url = self.url + title_link.attrs["href"]

            logging.debug(f"Found victim: {name}")

            # check if the org is already seen (search by url because name isn't guarenteed unique)
            q = self.session.query(Victim).filter_by(url=url, site=self.site)

            if q.count() == 0:
                # new org
                v = Victim(name=name, url=url, published=None, first_seen=datetime.utcnow(), last_seen=datetime.utcnow(), site=self.site)
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

            # get max page number
            page_list = soup.find("ul", class_="pagination")
            last_li = page_list.find_all("li")[-2]

            max_page_num = int(last_li.find("a").text)

            # start at the last page and go backwards, in case a new victim was added while running (unlikely but possible)
            for i in range(max_page_num, 0, -1):
                r = p.get(f"{self.url}?page={i}", headers=self.headers)

                self._handle_page(r.content.decode())
                
            # check one past the last page to see if new orgs were added that caused another page to be added
            r = p.get(f"{self.url}?page={max_page_num+1}", headers=self.headers)
            self._handle_page(r.content.decode())

        # just for good measure
        self.session.commit()
