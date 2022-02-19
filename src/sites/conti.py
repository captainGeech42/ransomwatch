from datetime import datetime
import logging
import re
import json

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

class Conti(SiteCrawler):
    actor = "Conti"

    def _handle_page(self, body: str):

        news_list = re.findall(r'newsList\(\s(\[.*\])\s\);', body)
        
        if len(news_list) > 0:
            news_list = json.loads(news_list[0])

            for elem in news_list:
                name = elem['title']
                published_dt = datetime.fromtimestamp(elem['date'])
                url = f"{self.url}{elem['url']}"
                
                logging.debug(f"Found victim: {name} ({url}) published at {published_dt}")

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

            self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            page_list = soup.find("ul", class_="pages")
            last_li = page_list.find_all("li")[-1]

            max_page_num = int(last_li.find("a").attrs["href"].split("/")[2])

            # start at the last page and go backwards, in case a new victim was added while running (unlikely but possible)
            for i in range(max_page_num, 0, -1):
                r = p.get(f"{self.url}/page/{i}", headers=self.headers)
                self._handle_page(r.content.decode())
                
            # check one past the last page to see if new orgs were added that caused another page to be added
            r = p.get(f"{self.url}/page/{max_page_num+1}", headers=self.headers)
            self._handle_page(r.content.decode())

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
