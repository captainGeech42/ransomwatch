import logging

from config import Config
from db.models import Site, Victim
from .slack import SlackNotification
from .discord import DiscordNotification

class NotificationManager():
    def send_new_victim_notification(victim: Victim):
        for dest, params in Config["notifications"].items():
            if not params["new_victims"]:
                continue

            if params["type"] == "slack":
                if not SlackNotification.send_new_victim_notification(params["url"], victim):
                    logging.error(f"Failed to send new victim notification to Slack workspace \"{dest}\"")
            elif params["type"] == "discord":
                if not DiscordNotification.send_new_victim_notification(params["url"], victim):
                    logging.error(f"Failed to send new victim notification to Discord guild \"{dest}\"")
            else:
                logging.error(f"Attempted to send a new victim notification to an unsupported notification type: {params['type']}")
    
    def send_victim_removed_notification(victim: Victim):
        for dest, params in Config["notifications"].items():
            if not params["removed_victims"]:
                continue

            if params["type"] == "slack":
                if not SlackNotification.send_victim_removed_notification(params["url"], victim):
                    logging.error(f"Failed to send removed victim notification to Slack workspace \"{dest}\"")
            elif params["type"] == "discord":
                if not DiscordNotification.send_victim_removed_notification(params["url"], victim):
                    logging.error(f"Failed to send removed victim notification to Discord guild \"{dest}\"")
            else:
                logging.error(f"Attempted to send a removed victim notification to an unsupported notification type: {params['type']}")
    
    def send_site_down_notification(site: Site):
        for dest, params in Config["notifications"].items():
            if not params["down_sites"]:
                continue

            if params["type"] == "slack":
                if not SlackNotification.send_site_down_notification(params["url"], site):
                    logging.error(f"Failed to send site down notification to Slack workspace \"{dest}\"")
            elif params["type"] == "discord":
                if not DiscordNotification.send_site_down_notification(params["url"], site):
                    logging.error(f"Failed to send site down notification to Discord guild \"{dest}\"")
            else:
                logging.error(f"Attempted to send a site down notification to an unsupported notification type: {params['type']}")
    
    def send_error_notification(context: str, error: str, fatal: bool = False):
        for dest, params in Config["notifications"].items():
            if not params["errors"]:
                continue

            if params["type"] == "slack":
                if not SlackNotification.send_error_notification(params["url"], context, error, fatal):
                    logging.error(f"Failed to send error notification to Slack workspace \"{dest}\"")
            elif params["type"] == "discord":
                if not DiscordNotification.send_error_notification(params["url"], context, error, fatal):
                    logging.error(f"Failed to send error notification to Discord guild \"{dest}\"")
            else:
                logging.error(f"Attempted to send a site down notification to an unsupported notification type: {params['type']}")