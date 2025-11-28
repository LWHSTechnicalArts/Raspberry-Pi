from raspc_notif import notif
from time import sleep
import subprocess

# Get your API key from RaspController app: Settings Notifications
sender = notif.Sender(apikey="YOUR API KEY HERE")

# Send a test notification
notification = notif.Notification(
    "Hello!", 
    "This is a test notification from my Raspberry Pi",
    high_priority=True
)

result = sender.send_notification(notification)

if result.status == notif.Result.SUCCESS:
    print("Notification sent successfully!")
else:
    print(f"Error: {result.message}")
