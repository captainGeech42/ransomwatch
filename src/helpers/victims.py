from datetime import datetime
from db.models import Victim


def append_victims(site, victim_leak_site, victim_name, published_dt):
    if victim_leak_site is None:
        q = site.session.query(Victim).filter_by(
            name=victim_name, site=site.site)
    else:
        q = site.session.query(Victim).filter_by(
            url=victim_leak_site, site=site.site)
    if q.count() == 0:
        # new victim
        v = Victim(name=victim_name, url=victim_leak_site, published=published_dt,
                   first_seen=datetime.utcnow(), last_seen=datetime.utcnow(), site=site.site)
        site.session.add(v)
        site.new_victims.append(v)
    else:
        # already seen, update last_seen
        v = q.first()
        v.last_seen = datetime.utcnow()
    site.current_victims.append(v)
