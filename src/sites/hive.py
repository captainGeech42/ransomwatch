from datetime import datetime
import logging

from config import Config
from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler

import helpers.victims as victims


class Hive(SiteCrawler):
    actor = "Hive"

    def __init__(self, url: str):
        super(Hive, self).__init__(url)

        self.headers["Accept"] = "application/json, text/plain, */*"
        self.headers["Origin"] = "null"
    
    def is_site_up(self) -> bool:
        # can't use the parent class is_site_up() because the / route doesn't exist on the API server
        with Proxy() as p:
            try:
                r = p.get(f"{self.url}/v1/companies/disclosed", headers=self.headers, timeout=Config["timeout"])

                if r.status_code >= 400:
                    return False
            except Exception as e:
                print(e)
                return False

        self.site.last_up = datetime.utcnow()

        return True

    def scrape_victims(self):
        with Proxy() as p:
            r = p.get(f"{self.url}/v1/companies/disclosed", headers=self.headers)

            j = r.json()

            for entry in j:
                name = entry["title"]
                url = entry["website"]

                logging.debug(f"Found victim: {name}")

                publish_dt = datetime.strptime(entry["disclosed_at"], "%Y-%m-%dT%H:%M:%SZ")

                victims.append_victims(self, url, name, publish_dt)
            
        self.site.last_scraped = datetime.utcnow()
        self.session.commit()
