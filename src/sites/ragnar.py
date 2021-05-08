from datetime import datetime
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


class Ragnar(SiteCrawler):
    actor = "Ragnar"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")
            
            script_list = soup.find_all("script")
            # they include the list in javascript code instead of HTML
            # So we have to parse it
            javascript_code = ""
            for script in script_list:
                script = str(script)
                if "var post_links = " in script:
                    javascript_code = script
                    break
            start_index = javascript_code.find("var post_links = ")
            end_index = javascript_code[start_index:].find("var baseUrl") + start_index
            javascript_code = javascript_code[start_index:end_index].strip()
            
            start_index = javascript_code.find("[")
            end_index = javascript_code.rfind("]") + 1
            javascript_code = javascript_code[start_index:end_index].strip().replace("null", "None")
            
            # convert javascript list of dictionary to python's list of dictionary
            victim_list = list(eval(javascript_code))

            for victim in victim_list:
                victim_name = victim["title"]
                
                if "-" in victim_name:
                    victim_name = victim_name[:victim_name.find("-")]
                
                published = int(victim["timestamp"])
                published_dt = datetime.utcfromtimestamp(published)

                victim_leak_site = self.url + "/?" + victim["link"] + "/"
                
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
