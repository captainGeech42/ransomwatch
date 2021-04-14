import logging
import sys

from db.database import Session
from db.models import Site, Victim
import sites

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y/%m/%d %H:%M:%S",
    handlers=[
        #logging.FileHandler(filename="enum.log", mode="a"),
        logging.StreamHandler()
    ]
)

defang = lambda u: u.replace("http", "hxxp").replace(".onion", "[.]onion")

def test():
    # s1 = Site(actor="site2", url="http://site1.onion")
    # print(s1)

    # v1 = Victim(org="org1", url="asdf/org1", first_seen=datetime.utcnow(), last_seen=datetime.utcnow(), site=s1)
    # print(v1)
    # print(v1.site)

    session = Session()
    # print(type(session))



    # session.add(s1)
    # session.add(v1)
    # session.commit()

    s1 = session.query(Site).filter_by(actor="site2").first()
    print(s1)
    print(type(s1))

    print(s1.victims)

def main(argv):
    logging.info("Initializing")

    sites_to_analyze = [
        sites.conti.Conti
    ]

    logging.info(f"Found {len(sites_to_analyze)} sites")

    for site in sites_to_analyze:
        logging.info(f"Starting scraping on {site.actor} ({defang(site.url)})")

        s = site()

        if not s.is_up:
            logging.warning(f"{site.actor} is down, skipping")
            continue

        logging.info(f"Scraping victims")
        s.scrape_victims()

        logging.info(f"Finished {site.actor}")

    logging.info("Finished all sites, exiting")
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))
