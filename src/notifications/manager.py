import logging

from config import Config
from db.models import Site, Victim
from .slack import SlackNotification

class NotificationManager():
    def send_new_victim_notification(victim: Victim):
        for workspace, params in Config["slack"].items():
            if not params["new_victims"]:
                continue

            if not SlackNotification.send_new_victim_notification(params["url"], victim):
                logging.error(f"Failed to send new victim notification to Slack workspace \"{workspace}\"")
    
    def send_victim_removed_notification(victim: Victim):
        for workspace, params in Config["slack"].items():
            if not params["removed_victims"]:
                continue

            if not SlackNotification.send_victim_removed_notification(params["url"], victim):
                logging.error(f"Failed to send removed victim notification to Slack workspace \"{workspace}\"")
    
    def send_site_down_notification(site: Site):
        for workspace, params in Config["slack"].items():
            if not params["down_sites"]:
                continue

            if not SlackNotification.send_site_down_notification(params["url"], site):
                logging.error(f"Failed to send site down notification to Slack workspace \"{workspace}\"")
    
    def send_error_notification(context: str, error: str, fatal: bool = False):
        for workspace, params in Config["slack"].items():
            if not params["errors"]:
                continue

            if not SlackNotification.send_error_notification(params["url"], context, error, fatal):
                logging.error(f"Failed to send error notification to Slack workspace \"{workspace}\"")