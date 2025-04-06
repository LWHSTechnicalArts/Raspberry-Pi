import smtplib
from email.mime.text import MIMEText

# Set up the message
msg = MIMEText("Hello from your Raspberry Pi!")
msg["From"] = "your_email@example.com"
msg["To"] = "1234567890@vtext.com"  # Replace with actual gateway
msg["Subject"] = "hello"

# Send the email (using Gmail SMTP as an example)
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login("your_email@example.com", "your_email_password")
    server.send_message(msg)

'''
AT&T: [number]@txt.att.net​
T-Mobile: [number]@tmomail.net​
Verizon: [number]@vtext.com​
Sprint: [number]@messaging.sprintpcs.com
'''
