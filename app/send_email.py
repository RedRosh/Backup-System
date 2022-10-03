import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "archivagebot@gmail.com"  # Enter your address
receiver_email = ["Omarelgribes07@gmail.com","ad.ezzaim@gmail.com"]  # Enter receiver address
password = 'tgkuspwabhnyvine'

message = """From: From Archivage Bot <daily_reminder@archivage.tse>
Subject: SMTP e-mail test

This is a test e-mail message.
"""
print('Sending email...')
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
print('Done.')

