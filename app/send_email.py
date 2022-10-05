import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "archivagebot@gmail.com"  # Enter your address
receivers_email = ["ad.ezzaim@gmail.com"]  # Enter receiver address
password = 'tgkuspwabhnyvine'

message = """From: From Archivage Bot <daily_reminder@archivage.tse>
Subject: TEST

this message is a test.
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receivers_email, message)


