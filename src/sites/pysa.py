from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

from bs4 import BeautifulSoup

from db.models import Victim
from net.proxy import Proxy
from .sitecrawler import SiteCrawler


class Pysa(SiteCrawler):
    actor = "Pysa"

    def scrape_victims(self):
        with Proxy() as p:
            url = self.url + '/partners.html'
            r = p.get(f"{url}", headers=self.headers)

            soup = BeautifulSoup(r.content.decode(), "html.parser")

            # get max page number
            victim_list = soup.find_all("div", class_="page-header")
            last_published_dt = None

            for victim in victim_list:
                victim_name = victim.find_all("a")[0].text.strip()
                published = victim.find_all("span")[1].text.strip()

                # they use a bunch of different date format...
                published_dt = None
                year_format = "%y"
                if len(published.split('/')[2]) == 4:
                    year_format = "%Y"
                try:
                    published_dt = datetime.strptime(
                        published, "%m/%d/{}".format(year_format))
                    # as we don't know the format of the date, let's check if the month detected
                    # is near the previous considered month
                    if last_published_dt and ((published_dt.month != last_published_dt.month)
                        or (published_dt.month != (last_published_dt + relativedelta(months=-1)).month)):
                        published_dt = datetime.strptime(
                            published, "%d/%m/{}".format(year_format))
                except ValueError as ve:
                    try:
                        published_dt = datetime.strptime(
                            published, "%d/%m/{}".format(year_format))
                    except ValueError as ve:
                        logging.error("Unable to cast date {}".format(published))

                last_published_dt = published_dt

                victim_leak_site = self.url + '/' + victim.find_all("a")[0].attrs["href"]
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
