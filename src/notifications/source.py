from db.models import Victim

# webhook/url only at this point, email or something in the future
# would require reworking config loading into something fancier
class NotificationSource():
    def send_new_victim_notification(victim: Victim, **kwargs) -> bool:
        raise Exception("Function implementation not found")
    
    def send_victim_removed_notification(victim: Victim, **kwargs) -> bool:
        raise Exception("Function implementation not found")
    
    def send_site_down_notification(info: str, **kwargs) -> bool:
        raise Exception("Function implementation not found")
    
    def send_error_notification(context: str, error: str, fatal: bool = False, **kwargs) -> bool:
        raise Exception("Function implementation not found")