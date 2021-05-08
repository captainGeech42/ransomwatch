from datetime import datetime
import logging
import requests
import time
from typing import Dict

from db.models import Site, Victim
from .source import NotificationSource

class DiscordNotification(NotificationSource):
    def _post_webhook(body: Dict, url: str) -> bool:
        r = requests.post(url, json=body)

        # check if we got rate limited
        if r.status_code == 429:
            logging.info("Got rate limited by Discord, sleeping 3 sec")
            time.sleep(1)
            return DiscordNotification._post_webhook(body, url)

        if r.status_code != 204:
            logging.error(
                f"Error sending Discord notification ({r.status_code}): {r.content.decode()}")
            return False

        return True

    def send_new_victim_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = {
            "embeds": [
                {
                    "title": "New Victim Posted",
                    "color": 238076,
                    "fields": [
                        {
                            "name": "Actor",
                            "value": victim.site.actor
                        },
                        {
                            "name": "Organization",
                            "value": victim.name
                        },
                        {
                            "name": "Published Date",
                            "value":  published_ts
                        },
                        {
                            "name": "First Seen",
                            "value": datetime.strftime(victim.first_seen, '%b %d, %Y at %H:%M:%S UTC')
                        },
                        {
                            "name": "View Victim Page",
                            "value": f"[Link]({victim.url})" if victim.url is not None else "(no link available)"
                        },
                        {
                            "name": "View Leak Site",
                            "value": f"[Link]({victim.site.url})"
                        },
                    ]
                }
            ]
        }

        return DiscordNotification._post_webhook(body, url)

    def send_victim_removed_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"
        
        body = {
            "embeds": [
                {
                    "title": "Victim Removed",
                    "color": 16100647,
                    "fields": [
                        {
                            "name": "Actor",
                            "value": victim.site.actor
                        },
                        {
                            "name": "Organization",
                            "value": victim.name
                        },
                        {
                            "name": "Date Originally Published",
                            "value":  published_ts
                        },
                        {
                            "name": "Last Seen",
                            "value": datetime.strftime(victim.last_seen, '%b %d, %Y at %H:%M:%S UTC')
                        },
                        {
                            "name": "View Leak Site",
                            "value": f"[Link]({victim.site.url})"
                        },
                    ]
                }
            ]
        }

        return DiscordNotification._post_webhook(body, url)

    def send_site_down_notification(url: str, site: Site) -> bool:
        last_up_ts = datetime.strftime(site.last_up, '%b %d, %Y at %H:%M:%S UTC') if site.last_up is not None else "N/A"
        
        body = {
            "embeds": [
                {
                    "title": "Site Down",
                    "color": 16564739,
                    "fields": [
                        {
                            "name": "Actor",
                            "value": site.actor
                        },
                        {
                            "name": "Last Up",
                            "value": last_up_ts
                        },
                        {
                            "name": "View Leak Site",
                            "value": f"[Link]({site.url})"
                        },
                    ]
                }
            ]
        }

        return DiscordNotification._post_webhook(body, url)

    def send_error_notification(url: str, context: str, error: str, fatal: bool = False) -> bool:
        body = {
            "embeds": [
                {
                    "title": f"{'Fatal ' if fatal else ''}Error",
                    "color": 16515843,
                    "description": f"**An error occurred:** {context}\n\n```{error}```\nFor more details, please check the app container logs\n\n_If you think this is a bug, please [open an issue](https://github.com/captainGeech42/ransomwatch/issues) on GitHub_",
                }
            ]
        }

        return DiscordNotification._post_webhook(body, url)