import logging
import sys

from config import Config
from db.database import Session
from db.models import Site, Victim
from net.slack import SlackNotification
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
        logging.info(f"Starting process for {site.actor}")

        if site.actor.lower() not in Config["sites"]:
            logging.warning(f"No URL found in config for this actor, skipping")

        s = site(Config["sites"][site.actor.lower()])
        
        if s.first_run:
            logging.info(f"This is the first scrape for {site.actor}")

        if not s.is_up:
            logging.warning(f"{site.actor} is down, skipping")
            continue

        logging.info(f"Scraping victims")
        s.scrape_victims()

        logging.info(f"There are {len(s.new_victims)} new victims")

        # send notifications for new victims
        if not s.first_run and len(s.new_victims) > 0:
            logging.info("Notifying for new victims")
            for v in s.new_victims:
                for workspace, slack_url in Config["slack"].items():
                    if not SlackNotification.send_new_victim_notification(slack_url, v):
                        logging.error(f"Failed to send Slack notification to {workspace}")
        
        logging.info(f"Identifying removed victims")
        removed = s.identify_removed_victims()
        logging.info(f"There are {len(removed)} removed victims")

        # send notifications for removed victims
        if not s.first_run and len(removed) > 0:
            logging.info("Notifying for removed victims")
            for v in removed:
                for workspace, slack_url in Config["slack"].items():
                    if not SlackNotification.send_victim_removed_notification(slack_url, v):
                        logging.error(f"Failed to send Slack notification to {workspace}")

        logging.info(f"Finished {site.actor}")

    logging.info("Finished all sites, exiting")
    
if __name__ == "__main__":
    # test()
    sys.exit(main(sys.argv))
