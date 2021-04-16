from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm.session import Session as SessionType

from config import Config
from db.database import Session
from db.models import Site, Victim
from net.proxy import Proxy

class SiteCrawler:
    # threat actor associated with the leak site
    actor: str = ""

    # url for the leak site
    url: str = ""

    # list of victims on the leak site from current scrape
    current_victims: List[Victim] = []

    # new victims on the leak site from current scrape
    new_victims: List[Victim] = []

    # is the site up? set by is_site_up()
    is_up: bool = False

    # db session, set in __init__()
    session: SessionType

    # site object from db, set in __init__()
    site: Site

    # is this the first ingest of the site? set in __init__()
    # if the first run, don't notify on new victims (b/c they are all "new")
    first_run: bool = False
    
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
    }

    def __init__(self, url: str):
        """
        make sure site is in db
        check if site is up
            if it is, update last_up in db
        """

        # this should be statically defined in child implementations of the class
        assert self.actor != ""

        self.current_victims = []
        self.new_victims = []

        self.url = url

        self.session = Session()

        q = self.session.query(Site).filter_by(actor=self.actor)

        if q.count() == 0:
            # site is new, init obj
            self.site = Site(actor=self.actor, url=self.url)
            self.session.add(self.site)
            self.session.commit()
            self.first_run = True
        else:
            # site exists, set obj
            self.site = q.first()

            # if we haven't successfully scraped the site before, consider this the first run
            if self.site.last_scraped is None:
                self.first_run = True

        # check if site is up
        self.is_up = self.is_site_up()

    def is_site_up(self) -> bool:
        """
        check if the site is up

        this might have specific criteria for some sites
        """

        with Proxy() as p:
            try:
                r = p.get(self.url, headers=self.headers, timeout=Config["timeout"])

                if r.status_code >= 400:
                    return False
            except Exception as e:
                return False

        self.site.last_up = datetime.utcnow()

        return True

    def scrape_victims(self):
        """
        pull each listing on the site
        check if its already in the db
            if it is, update the last seen
            if it isn't, add it to the db

        store each org name in a list (self.current_victims)

        this also sets self.new_victims, which has new victims to notify with
        """
        raise Exception("Function implementation not found")

    def identify_removed_victims(self) -> List[Victim]:
        """
        check org name list against db
            if something is in the db, not already removed, and not in the list, alert
        """
        # get the current victims from the last scrape
        victims = self.session.query(Victim).filter_by(site=self.site, removed=False).all()

        # remove anything from the last scrape that was also in this scrape
        # the remaining set is things that were present last time, but not this time
        for v in self.current_victims:
            try:
                victims.remove(v)
            except ValueError:
                # i think there is an edge case here that can be caused by
                # running the scrape while a victim is removed
                # it _should_ get picked up on the next run though, so we
                # can safely ignore this
                pass

        # mark the victims as removed, since they are no longer on the leak site
        for v in victims:
            v.removed = True

        self.session.commit()

        return victims