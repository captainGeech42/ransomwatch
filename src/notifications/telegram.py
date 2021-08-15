from datetime import datetime
import logging
import requests

from db.models import Site, Victim
from .source import NotificationSource

class TelegramNotification(NotificationSource):

    def _send_msg(msg, apikey=None, chatid=None):
        url = f"https://api.telegram.org/bot{apikey}/sendMessage"
        data = {
            'chat_id': str(chatid),
            'disable_web_page_preview': False,
            'disable_notification': False,
            'parse_mode':'HTML',
            'text': msg
        }
        r = requests.post(url, data)
        # check status code
        if r.status_code != 200:
            logging.error(
                f"Error sending Telegram notification ({r.status_code}): {r.content.decode()}")
            return False            
        return True

    def send_new_victim_notification(victim: Victim, apikey: str, chatid: str) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"
        body = f"\U0001F514 <b>New Victim Posted</b>\n" \
               f"<b>Actor:</b> {victim.site.actor}\n" \
               f"<b>Organization:</b> {victim.name}\n" \
               f"<b>Published Date:</b> {published_ts}\n" \
               f"<b>First Seen:</b> " + datetime.strftime(victim.first_seen, '%b %d, %Y at %H:%M:%S UTC') + "\n" \
               f"<b>Leak Site:</b> <a href=\"{victim.site.url}\">Link</a>\n"
        if victim.url is not None:
            body += f"<b>Victim Page:</b> <a href=\"{victim.url}\">Link</a>\n"
        else:
            body += f"<b>Victim Page:</b> (no link available)\n"

        return TelegramNotification._send_msg(body, apikey, chatid)

    def send_victim_removed_notification(victim: Victim, apikey: str, chatid: str) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"
        body = f"\U0001F515 <b>Victim Removed</b>\n" \
               f"<b>Actor:</b> {victim.site.actor}\n" \
               f"<b>Organization:</b> {victim.name}\n" \
               f"<b>Published Date:</b> {published_ts}\n" \
               f"<b>Last Seen:</b> " + datetime.strftime(victim.last_seen, '%b %d, %Y at %H:%M:%S UTC') + "\n" \
               f"<b>Leak Site:</b> <a href=\"{victim.site.url}\">Link</a>\n"
        return TelegramNotification._send_msg(body, apikey, chatid)

    def send_site_down_notification(site: Site, apikey: str, chatid: str) -> bool:
        last_up_ts = datetime.strftime(site.last_up, '%b %d, %Y at %H:%M:%S UTC') if site.last_up is not None else "N/A"
        body = f"\U0001F6A7 <b>Site Down</b>\n" \
               f"<b>Actor:</b> {site.actor}\n" \
               f"<b>Last Up:</b> {last_up_ts}\n" \
               f"<b>Leak Site:</b> <a href=\"{site.url}\">Link</a>\n"
        return TelegramNotification._send_msg(body, apikey, chatid)

    def send_error_notification(context: str, error: str, fatal: bool = False, apikey: str = None, chatid: str = None) -> bool:
        body = f"\U000026A0 <b>{'Fatal ' if fatal else ''}Error</b>\n" \
               f"<b>An error occurred:</b> {context}\n\n```{error}```\nFor more details, please check the app container logs\n\n_If you think this is a bug, please <a href=\"https://github.com/captainGeech42/ransomwatch/issues\">open an issue</a>) on GitHub_"
        return TelegramNotification._send_msg(body, apikey, chatid)
