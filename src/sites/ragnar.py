from datetime import datetime
import json
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler
import helpers.victims as victims


class Ragnar(SiteCrawler):
    actor = "Ragnar"

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")
            
            script_list = soup.find_all("script")
            # they include the list in javascript code instead of HTML
            # So we have to parse it
            js_victims_raw = ""
            js_marker = "var post_links = "

            for script in script_list:
                script = str(script)
                if js_marker in script:
                    js_victims_raw = script
                    break

            if not js_victims_raw:
                raise Exception(f"js victim list not found (tried to locate '{js_marker}')")

            raw_victim_list = js_victims_raw.split(f"{js_marker}[{{")[1].split(
                "}]"
            )[0]
            victim_list = json.loads(f"[{{{raw_victim_list}}}]")

            for victim in victim_list:
                victim_name = victim["title"]
                
                if "-" in victim_name:
                    victim_name = victim_name[:victim_name.find("-")]
                
                published = int(victim["timestamp"])
                published_dt = datetime.utcfromtimestamp(published)

                victim_leak_site = self.url + "/?" + victim["link"] + "/"
                
                victims.append_victims(self, victim_leak_site, victim_name, published_dt)
            self.session.commit()

        self.site.last_scraped = datetime.utcnow()

        # just for good measure
        self.session.commit()
