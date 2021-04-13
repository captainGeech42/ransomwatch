import base64
from datetime import datetime
import logging
import sys
import time

from bs4 import BeautifulSoup

from net.proxy import Proxy

from db.database import Session
from db.models import Site, Leak

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y/%m/%d %H:%M:%S",
    handlers=[
        #logging.FileHandler(filename="enum.log", mode="a"),
        logging.StreamHandler()
    ]
)

def print_ip():
    with Proxy() as p:
        print(p.get("http://icanhazip.com").content.decode().strip())

def main(argv):
    s1 = Site(actor="site1", url="http://site1.onion")
    print(s1)

    l1 = Leak(org="org1", url="asdf/org1", first_seen=datetime.utcnow(), last_seen=datetime.utcnow(), site=s1)
    print(l1)
    print(l1.site)

    session = Session()

    session.add(s1)
    session.add(l1)
    session.commit()

    return 0
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))
