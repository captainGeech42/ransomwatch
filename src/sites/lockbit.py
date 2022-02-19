import re
from datetime import datetime
from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
from config import Config

from playwright.sync_api import sync_playwright


class Lockbit(SiteCrawler):
    actor = "Lockbit"

    def _handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("div", class_="post-block")

        for victim in victim_list:
            victim_name = victim.find("div", class_="post-title").text.strip()
            victim_leak_site = f'{self.url}{victim.find("div", class_="post-block-body").find("a").attrs["href"]}'
            published_dt= datetime.now()
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
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy={"server": f'socks://{Config["proxy"]["hostname"]}:{Config["proxy"]["socks_port"]}'})
            page = browser.new_page()
            page.set_extra_http_headers(self.headers) 
            page.goto(self.url)
            
            welcome_page_countdown = re.findall(r"let counter = (\d)\s", page.content())
            welcome_page_countdown = ((int(welcome_page_countdown[0]) * 1000) + 500) if len(welcome_page_countdown) > 0 else 10000 # 10s as a timeout fallback value
            page.wait_for_timeout(welcome_page_countdown)
            res = page.content()

            soup = BeautifulSoup(res, "html.parser")

            # find all pages
            page_nav = soup.find_all("a", class_="page-numbers")

            site_list = []
            site_list.append(self.url)
            
            for page in page_nav:
                # might exist repetition
                if page.attrs["href"] not in site_list:
                    site_list.append(page.attrs["href"])
            
            for site in site_list:
                page.goto(site)
                r = page.content()
                self._handle_page(r) 

            browser.close()
            self.site.last_scraped = datetime.utcnow()

