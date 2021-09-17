from datetime import datetime
import logging
import requests
from typing import Dict
import json

from db.models import Site, Victim
from .source import NotificationSource

class TeamsNotification(NotificationSource):

    def _escape_url(url:str) -> str:
        url_rep = url.replace("http", "hxxp").replace(".", "[.]")
        return url_rep

    def _send_message_by_incomingwebhook(url:str,message:str) -> requests.models.Response:
        headers={"Content-type": "application/json"}
        params={"text":message}
        response=TeamsNotification._post(url,headers=headers,params=json.dumps(params))
        return response

    def _post(url:str, headers:dict = None, params:dict = None) -> requests.models.Response:
        if headers:
            response=requests.post(url,headers=headers,data=params)
        else :
            response=requests.post(url,data=params)

        return response

    def _post_webhook(body: str, url: str) -> bool:
        r = TeamsNotification._send_message_by_incomingwebhook(url, body)
        if r.status_code != 200:
            logging.error(f"Error sending Teams notification ({r.status_code}): {r.content.decode()}")
            return False

        return True


    def send_new_victim_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = f'''*■New Victim Posted*\n
  Actor: {victim.site.actor}\n
  Organization: {victim.name}\n
  Published Date: {published_ts}\n
  First Seen: {datetime.strftime(victim.first_seen, '%b %d, %Y at %H:%M:%S UTC')}\n
  View Victim Page: {TeamsNotification._escape_url(victim.url) if victim.url is not None else "(no victim link available)"}\n
  View Leak Site: {TeamsNotification._escape_url(victim.site.url)}'''

        return TeamsNotification._post_webhook(body, url)

    def send_victim_removed_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = f'''*■Victim Removed*\n
Actor: {victim.site.actor}\n
Organization: {victim.name}\n
Date Originally Published: {published_ts}\n
Last Seen: {datetime.strftime(victim.last_seen, '%b %d, %Y at %H:%M:%S UTC')}\n
View Leak Site: {TeamsNotification._escape_url(victim.site.url)}'''

        return TeamsNotification._post_webhook(body, url)

    def send_site_down_notification(url: str, site: Site) -> bool:
        last_up_ts = datetime.strftime(site.last_up, '%b %d, %Y at %H:%M:%S UTC') if site.last_up is not None else "N/A"

        body = f'''*■Site Down*\n
Actor: {site.actor}\n
View Leak Site: {TeamsNotification._escape_url(site.url)}'''

        return TeamsNotification._post_webhook(body, url)

    def send_error_notification(url: str, context: str, error: str, fatal: bool = False) -> bool:
        body = f'''{'*■Fatal* ' if fatal else ''}Error
An error occurred: {context}\n
```{error}```\nFor more details, please check the app container logs\n
If you think this is a bug, please on GitHub open an issue:https://github.com/lac-japan/ransomwatch/issues'''

        return TeamsNotification._post_webhook(body, url)
