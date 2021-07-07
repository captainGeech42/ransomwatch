import logging

from config import Config
from db.models import Site, Victim
from .slack import SlackNotification
from .discord import DiscordNotification
from .telegram import TelegramNotification
from .mattermost import MattermostNotification

class NotificationManager():
    def send_new_victim_notification(victim: Victim):
        if "notifications" in Config and Config["notifications"]:
            for dest, params in Config["notifications"].items():
                if not params["new_victims"]:
                    continue

                if params["type"] == "slack":
                    if not SlackNotification.send_new_victim_notification(victim, url=params["url"]):
                        logging.error(f"Failed to send new victim notification to Slack workspace \"{dest}\"")
                elif params["type"] == "discord":
                    if not DiscordNotification.send_new_victim_notification(victim, url=params["url"]):
                        logging.error(f"Failed to send new victim notification to Discord guild \"{dest}\"")
                elif params["type"] == "telegram":
                    if not TelegramNotification.send_new_victim_notification(victim, apikey=params["telegram_apikey"], chatid=params["telegram_chatid"]):
                        logging.error(f"Failed to send new victim notification to Telegram chat \"{dest}\"")
                elif params["type"] == "mattermost":
                   if not MattermostNotification.send_new_victim_notification(victim, url=params["url"], username=params['mattermost_username'], channel=params['mattermost_channel']):
                        logging.error(f"Failed to send new victim notification to Mattermost chat \"{dest}\"")          
                else:
                    logging.error(f"Attempted to send a new victim notification to an unsupported notification type: {params['type']}")
    
    def send_victim_removed_notification(victim: Victim):
        if "notifications" in Config and Config["notifications"]:
            for dest, params in Config["notifications"].items():
                if not params["removed_victims"]:
                    continue

                if params["type"] == "slack":
                    if not SlackNotification.send_victim_removed_notification(victim, url=params["url"]):
                        logging.error(f"Failed to send removed victim notification to Slack workspace \"{dest}\"")
                elif params["type"] == "discord":
                    if not DiscordNotification.send_victim_removed_notification(victim, url=params["url"]):
                        logging.error(f"Failed to send removed victim notification to Discord guild \"{dest}\"")
                elif params["type"] == "telegram":
                    if not TelegramNotification.send_victim_removed_notification(victim, apikey=params["telegram_apikey"], chatid=params["telegram_chatid"]):
                        logging.error(f"Failed to send removed victim notification to Telegram chat \"{dest}\"")
                elif params["type"] == "mattermost":
                   if not MattermostNotification.send_victim_removed_notification(victim, url=params["url"], username=params['mattermost_username'], channel=params['mattermost_channel']):
                        logging.error(f"Failed to send removed victim notification to Mattermost chat \"{dest}\"")
                else:
                    logging.error(f"Attempted to send a removed victim notification to an unsupported notification type: {params['type']}")
    
    def send_site_down_notification(site: Site):
        if "notifications" in Config and Config["notifications"]:
            for dest, params in Config["notifications"].items():
                if not params["down_sites"]:
                    continue

                if params["type"] == "slack":
                    if not SlackNotification.send_site_down_notification(site, url=params["url"]):
                        logging.error(f"Failed to send site down notification to Slack workspace \"{dest}\"")
                elif params["type"] == "discord":
                    if not DiscordNotification.send_site_down_notification(site, url=params["url"]):
                        logging.error(f"Failed to send site down notification to Discord guild \"{dest}\"")
                elif params["type"] == "telegram":
                    if not TelegramNotification.send_site_down_notification(site, apikey=params["telegram_apikey"], chatid=params["telegram_chatid"]):
                        logging.error(f"Failed to send site down notification to Telegram chat \"{dest}\"")
                elif params["type"] == "mattermost":
                   if not MattermostNotification.send_site_down_notification(site, url=params["url"], username=params['mattermost_username'], channel=params['mattermost_channel']):
                        logging.error(f"Failed to send site down notification to Mattermost chat \"{dest}\"")
                else:
                    logging.error(f"Attempted to send a site down notification to an unsupported notification type: {params['type']}")
    
    def send_error_notification(context: str, error: str, fatal: bool = False):
        if "notifications" in Config and Config["notifications"]:
            for dest, params in Config["notifications"].items():
                if not params["errors"]:
                    continue

                if params["type"] == "slack":
                    if not SlackNotification.send_error_notification(context, error, fatal, url=params["url"]):
                        logging.error(f"Failed to send error notification to Slack workspace \"{dest}\"")
                elif params["type"] == "discord":
                    if not DiscordNotification.send_error_notification(context, error, fatal, url=params["url"]):
                        logging.error(f"Failed to send error notification to Discord guild \"{dest}\"")
                elif params["type"] == "telegram":
                    if not TelegramNotification.send_error_notification(context, error, fatal, apikey=params["telegram_apikey"], chatid=params["telegram_chatid"]):
                        logging.error(f"Failed to send error notification to Telegram chat \"{dest}\"")
                elif params["type"] == "mattermost":
                   if not MattermostNotification.send_error_notification(context, error, fatal, url=params["url"], username=params['mattermost_username'], channel=params['mattermost_channel']):
                        logging.error(f"Failed to send error notification to Mattermost chat \"{dest}\"")              
                else:
                    logging.error(f"Attempted to send error notification to an unsupported notification type: {params['type']}")