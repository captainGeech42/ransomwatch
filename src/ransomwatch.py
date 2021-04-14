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
    session = Session()

    site = session.query(Site).filter_by(actor="Conti").first()

    q = session.query(Victim).filter_by(site=site).all()

def main(argv):
    logging.info("Initializing")

    sites_to_analyze = [
        sites.conti.Conti
    ]

    logging.info(f"Found {len(sites_to_analyze)} sites")

    for site in sites_to_analyze:
        logging.info(f"Starting scraping on {site.actor} ({defang(site.url)})")

        s = site()
        
        if s.first_run:
            logging.info(f"This is the first scrape for {site.actor}")

        if not s.is_up:
            logging.warning(f"{site.actor} is down, skipping")
            continue

        logging.info(f"Scraping victims")
        s.scrape_victims()

        logging.info(f"There are {len(s.new_victims)} new victims")
        
        logging.info(f"Identifying removed victims")
        removed = s.identify_removed_victims()
        logging.info(f"There are {len(removed)} removed victims")

        logging.info(f"Finished {site.actor}")

    logging.info("Finished all sites, exiting")
    
if __name__ == "__main__":
    # test()
    sys.exit(main(sys.argv))
