import json
import csv
import datetime
import smtplib
import ssl
import ast
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from struct import pack

action = str(sys.argv[1])
server_ip = str(sys.argv[2])
error_msg = str(sys.argv[3])

sender_email = "saurabh.development.17@gmail.com"
password = "Mansi@2615"
sender = "saurabh.development.17@gmail.com"
receivers = "saurabhshirke158@gmail.com"
server = smtplib.SMTP('smtp.gmail.com:587')
# sender = 'sgsalt201@capitaland.com'
# receivers = ['saurabh.shirke@global.ntt']
# server = smtplib.SMTP('smtp.dc.capitaland.com')

def email_send_services(server_ip, error_msg):
    print(error_msg)
    subject = 'Ansible: Alert! Some services failed to restart for '+server_ip
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    html = """\
            <html>
            <head></head>
            <body>
                <p>Hi!<br><br>
                Following services failed to start after patching and rebooting the server """+server_ip+""". <br><br>
                Services failed to start automatically: """+error_msg+""".
                </p><br>
                <p>
                Please do not reply to this mail as this is an automated mail service
                </P>
            </body>
            </html>
            """
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    # message = 'Subject: {}\n\n{}'.format(subject, body)
    print(error_msg)
    if error_msg != '[]':
        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")
        except Exception as e:
            print(e)
        finally:
            server.quit()
    else:
        sys.exit

def email_send_connection(server_ip, error_msg):
    subject = 'Ansible: Alert! Server failed with prerequisites verification.'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    html = """\
            <html>
            <head></head>
            <body>
                <p>Hi!<br><br>
                Server """+server_ip+""" failed to connect and is unreachable. <br><br>
                Connection failure reason: """+error_msg+""".
                </p><br>
                <p>
                Please do not reply to this mail as this is an automated mail service
                </P>
            </body>
            </html>
            """
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    # message = 'Subject: {}\n\n{}'.format(subject, body)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        # server.login(sender_email, password)
        server.sendmail(sender, receivers, msg.as_string())
        print("Successfully sent email")
    except Exception as e:
        print(e)
    finally:
        server.quit()

if action == 'alert_connection':
    email_send_connection(server_ip, error_msg)
elif action == 'alert_services':
    email_send_services(server_ip, error_msg)
    print(error_msg)
