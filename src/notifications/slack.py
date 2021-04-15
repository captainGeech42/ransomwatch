from datetime import datetime
import logging
import requests
from typing import Dict

from db.models import Site, Victim
from .source import NotificationSource

class SlackNotification(NotificationSource):
    def _post_webhook(body: Dict, url: str) -> bool:
        r = requests.post(url, json=body)
        if r.status_code != 200:
            logging.error(
                f"Error sending Slack notification ({r.status_code}): {r.content.decode()}")
            return False

        return True

    def send_new_victim_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = {
            "attachments": [
                {
                    "color": "#03a1fc",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "New Victim Posted"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Actor:*\n{victim.site.actor}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Organization:*\n{victim.name}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Published Date:*\n{published_ts}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*First Seen:*\n{datetime.strftime(victim.first_seen, '%b %d, %Y at %H:%M:%S UTC')}"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"<{victim.url}|View Victim Page>"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"<{victim.site.url}|View Leak Site>"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return SlackNotification._post_webhook(body, url)

    def send_victim_removed_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = {
            "attachments": [
                {
                    "color": "#f5ad27",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Victim Removed"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Actor:*\n{victim.site.actor}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Organization:*\n{victim.name}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Date Originally Published:*\n{published_ts}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Last Seen:*\n{datetime.strftime(victim.last_seen, '%b %d, %Y at %H:%M:%S UTC')}"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"<{victim.site.url}|View Leak Site>"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return SlackNotification._post_webhook(body, url)

    def send_site_down_notification(url: str, site: Site) -> bool:
        last_up_ts = datetime.strftime(site.last_up, '%b %d, %Y at %H:%M:%S UTC') if site.last_up is not None else "N/A"

        body = {
            "attachments": [
                {
                    "color": "#fcc203",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Site Down"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Actor:*\n{site.actor}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Last Up:*\n{last_up_ts}"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"<{site.url}|View Leak Site>"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return SlackNotification._post_webhook(body, url)

    def send_error_notification(url: str, context: str, error: str, fatal: bool = False) -> bool:
        body = {
            "attachments": [
                {
                    "color": "#fc0303",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"{'Fatal ' if fatal else ''}Error"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*An error occurred:* {context}"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"```{error}```\nFor more details, please check the app container logs"
                            }
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": "If you think this is a bug, please <https://github.com/captainGeech42/ransomwatch/issues|open an issue> on GitHub"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return SlackNotification._post_webhook(body, url)