from datetime import datetime
import logging
import requests

from db.models import Site, Victim
from .source import NotificationSource

class MattermostNotification(NotificationSource):
    def _post_webhook(body: dict, url: str) -> bool:
        r = requests.post(url, json=body)
        if r.status_code != 200:
            logging.error(
                f"Error sending Mattermost notification ({r.status_code}): {r.content.decode()}")
            return False

        return True

    def send_new_victim_notification(victim: Victim, url: str, channel: str, username: str) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"
        
        body = f":bell: **New Victim Posted**\n" \
               f"**Actor:** {victim.site.actor}\n" \
               f"**Organization:** {victim.name}\n" \
               f"**Published Date:** {published_ts}\n" \
               f"**First Seen:** " + datetime.strftime(victim.first_seen, '%b %d, %Y at %H:%M:%S UTC') + "\n" \
               f"**Leak Site:** [Link]({victim.site.url})\n"
        if victim.url is not None:
            body += f"**Victim Page:** [Link]({victim.url})\n"
        else:
            body += f"**Victim Page:** *no link available*\n"

        payload={
            "channel": channel,
            "username": username,
            "text": body
        }
        return MattermostNotification._post_webhook(payload, url)

    def send_victim_removed_notification(victim: Victim, url: str, channel: str, username: str) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = f":no_bell: **Victim Removed**\n" \
               f"**Actor:** {victim.site.actor}\n" \
               f"**Organization:** {victim.name}\n" \
               f"**Published Date:** {published_ts}\n" \
               f"**Last Seen:** " + datetime.strftime(victim.last_seen, '%b %d, %Y at %H:%M:%S UTC') + "\n" \
               f"**Leak Site:** [Link]({victim.site.url})\n"

        payload={
            "channel": channel,
            "username": username,
            "text": body
        }
        return MattermostNotification._post_webhook(payload, url)

    def send_site_down_notification(site: Site, url: str, channel: str, username: str) -> bool:
        last_up_ts = datetime.strftime(site.last_up, '%b %d, %Y at %H:%M:%S UTC') if site.last_up is not None else "N/A"

        body = f":construction: **Site Down**\n" \
               f"**Actor:** {site.actor}\n" \
               f"**Last Up:** {last_up_ts}\n" \
               f"**Leak Site:** [Link]({site.url})\n"
        payload={
            "channel": channel,
            "username": username,
            "text": body
        }
        return MattermostNotification._post_webhook(payload, url)

    def send_error_notification(context: str, error: str, fatal: bool = False, url: str = None, channel: str = None, username: str = None) -> bool:
        body = f":warning: **{'Fatal ' if fatal else ''}Error**\n" \
               f"**An error occurred:** {context}\n\n```{error}```\nFor more details, please check the app container logs\n\n_If you think this is a bug, please [open an issue](https://github.com/captainGeech42/ransomwatch/issues) on GitHub_"
        payload={
            "channel": channel,
            "username": username,
            "text": body
        }
        return MattermostNotification._post_webhook(payload, url)
