from datetime import datetime
import logging
import re
from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

import helpers.victims as victims
import helpers.pagination as pagination


class Lorenz(SiteCrawler):
    actor = "Lorenz"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")
        victim_list = soup.find_all("div", {"id": re.compile("comp.*")})

        for victim in victim_list:
            victim_h3 = victim.find("div", class_="panel-heading").find("h3")
            if victim_h3 is None:
                # unpublished victims are in a h4
                continue
            victim_name = victim_h3.text.strip()
            victim_leak_site = self.url + "/#" + victim.get("id")

            if victim.find("span", class_="glyphicon"):
                published = victim.find("span", class_="glyphicon").next_sibling
                published = published.lstrip()
                published_dt = datetime.strptime(published, "Posted %b %d, %Y.")
            else:
                published_dt = None

            victims.append_victims(self, victim_leak_site, victim_name, published_dt)
        self.session.commit()

    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p)
