from datetime import datetime
import logging
from bs4 import BeautifulSoup
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims
import helpers.pagination as pagination


class Suncrypt(SiteCrawler):
    actor = "Suncrypt"

    def handle_page(self, body: str):
        soup = BeautifulSoup(body, "html.parser")
        
        victim_list = soup.find_all("div", class_="card mb-5")
        
        for victim in victim_list:
            victim_name = victim.find("div", class_="title is-4").text.strip()

            victim_leak_site = self.url + "/" + victim.find("div", class_="title is-4").find("a").attrs["href"]

            victims.append_victims(self, victim_leak_site, victim_name, None)
        self.session.commit()
    
    def scrape_victims(self):
        with Proxy() as p:
            pagination.handle_pages_for(self, p, "pagination-link")
