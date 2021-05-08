from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


class Cuba(SiteCrawler):
    actor = "Cuba"

    def extract_published_date(self, body: str):
        soup = BeautifulSoup(body, "html.parser")

        p_lines = soup.find_all("p")
        
        published = None
        
        for line in p_lines:
            line_description = line.text.strip()
            # They hard-code everything
            if "Date" in line_description:
                published = line_description[len("Date the files were received: "):]
                break
        
        if "." in published:
            published = published.replace(".", "")
            
            
        date_split = published.split(" ")
        
        day = date_split[0]
        month = date_split[1]
        year = date_split[2]
        
        if "-" in day:
            day = day.split("-")[0]
            
        if month == "01":
            month = "January"
        
        if month == "febriary":
            month = "February"
           
        published = day + " " + month + " " + year
           
        return datetime.strptime(published, "%d %B %Y")
            
    
    def _handle_page(self, body: str, p: Proxy):
        soup = BeautifulSoup(body, "html.parser")

        victim_list = soup.find_all("div", class_="list-text")
        
        for victim in victim_list:
            victim_description = victim.find("a").find("p").text.strip().split(" ")
            
            # extract company name by getting only the first few words that start with a capitalized letter
            victim_name = ""
            
            for word in victim_description:
                if word[0].isupper() or word == "and":
                    victim_name += word + " "
                else:
                    break
                
            victim_name = victim_name[:-1] # Delete the last space
            
            
            if victim_name[-2:] == "is":
                # hard-code this. They forgot to add a space to one name, so I can't properly scrape it
                victim_name = victim_name[:-2]
                
            
            # they put the published date in the victim's leak page
            victim_leak_site = victim.find("a").attrs["href"]
            
            r = p.get(victim_leak_site, headers=self.headers)
            published_dt = self.extract_published_date(r.content.decode())
            

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

            inner_sites = soup.find_all("div", class_="ajax-load-more-wrap default")
            
            for site in inner_sites:
                site_url = site.attrs["data-canonical-url"]
                r = p.get(site_url, headers=self.headers)
                self._handle_page(r.content.decode(), p)