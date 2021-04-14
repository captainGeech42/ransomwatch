from datetime import datetime
import logging
import requests

from db.models import Victim

class SlackNotification():
    def send_new_victim_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = {
        	"blocks": [
        		{
        			"type": "header",
        			"text": {
        				"type": "plain_text",
        				"text": "New Victim Posted",
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

        r = requests.post(url, json=body)
        if r.status_code != 200:
            logging.error(f"Error sending Slack notification ({r.status_code}): {r.content.decode()}")
            return False

        return True
    
    def send_victim_removed_notification(url: str, victim: Victim) -> bool:
        published_ts = datetime.strftime(victim.published, '%b %d, %Y') if victim.published is not None else "N/A"

        body = {
        	"blocks": [
        		{
        			"type": "header",
        			"text": {
        				"type": "plain_text",
        				"text": "Victim Removed",
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

        r = requests.post(url, json=body)
        if r.status_code != 200:
            logging.error(f"Error sending Slack notification ({r.status_code}): {r.content.decode()}")
            return False

        return True