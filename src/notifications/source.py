from db.models import Victim

# webhook/url only at this point, email or something in the future
# would require reworking config loading into something fancier
class NotificationSource():
    def send_new_victim_notification(url: str, victim: Victim) -> bool:
        raise Exception("Function implementation not found")
    
    def send_victim_removed_notification(url: str, victim: Victim) -> bool:
        raise Exception("Function implementation not found")
    
    def send_site_down_notification(url: str, info: str) -> bool:
        raise Exception("Function implementation not found")
    
    def send_error_notification(url: str, context: str, error: str, fatal: bool = False) -> bool:
        raise Exception("Function implementation not found")