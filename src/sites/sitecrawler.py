import requests
from typing import Dict, List

from sqlalchemy.orm.session import Session as SessionType

from db.database import Session
from db.models import Site
from net.proxy import Proxy

class SiteCrawler:
    actor: str = ""
    url: str = ""
    current_victims: List[str] = {}
    is_up: bool = False
    session: SessionType
    site: Site
    
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
    }

    def __init__(self):
        """
        make sure site is in db
        check if site is up
            if it is, update last_up in db
        """

        # these should be statically defined in child implementations of the class
        assert self.actor != ""
        assert self.url != ""

        self.session = Session()

        q = self.session.query(Site).filter_by(actor=self.actor)

        if q.count() == 0:
            # site is new, init obj
            self.site = Site(actor=self.actor,url=self.url)
            self.session.add(self.site)
            self.session.commit()
        else:
            # site exists, set obj
            self.site = q.first()

        # check if site is up
        self.is_up = self.site_is_up()

    def site_is_up(self) -> bool:
        """
        check if the site is up

        this might have specific criteria for some sites
        """

        with Proxy() as p:
            try:
                r = p.get(self.url, headers=self.headers, timeout=20)

                if r.status_code < 400:
                    return False
            except:
                return False

        return True

    def scrape_victims(self):
        """
        pull each listing on the site
        check if its already in the db
            if it is, update the last seen
            if it isn't, add it to the db

        store each org name in a list (self.current_victims)
        """
        pass

    def identify_removed_victims(self):
        """
        check org name list against db
            if something is in the db and not in the list, alert
        """
        pass