import json
import csv
import datetime
import smtplib
import ssl
import ast
import re
import sys
from struct import pack
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email_send_patching_failed(server_ip, error_msg):
    sender_email = "#Add SMTP Email here#"
    password = "#Add SMTP Pass here#"
    sender = '#Add Sender Email here#'
    receivers = '#Add Receiver Email here#'
    server = smtplib.SMTP('smtp.gmail.com:587')

    subject = 'Ansible: Alert! Server patching failed for '+server_ip
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    html = """\
            <html>
            <head></head>
            <body>
                <p>Hi!<br><br>
                Server """+server_ip+""" patching is failed. <br><br>
                Patching failure reason: """+error_msg+""".
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
        server.login(sender_email, password)
        server.sendmail(sender, receivers, msg.as_string())
        print("Successfully sent email")
    except Exception as e:
        print(e)
    finally:
        server.quit()


date = datetime.datetime.now()
current_date = date.strftime("%m-%d-%Y %H:%M:%S")
file_date = date.strftime("%Y_%m_%d_%H")
file_name = str(sys.argv[1]) 
file = open(file_name, 'r')

servers = file.readlines()
#x = json.loads(x[0])
row = []

for server in servers:
    # res = json.loads(server)
    try:
        res = ast.literal_eval(server)
    except:
        res = json.loads(server)

    if "unreachable" in res["data"]:
        server_name = res["server_name"]
        server_ip = res["ip"]
        server_os = res["os_distribution"]
        package_name = "-"
        patch_run = ""
        status = "Failed"
        comment = res["data"]["msg"]
        msg = "Server " + server_name + "is unreachable. Patching failed. Error message:" + res["data"]["msg"]
    elif res["data"]["failed"] == "True":
        server_name = res["server_name"]
        server_ip = res["ip"]
        server_os = res["os_distribution"]
        package_name = "-"
        patch_run = ""
        status = "Failed"
        comment = res["data"]["msg"]
        msg = "Server " + server_name + " patching failed. Error message:" + res["data"]["msg"]
        
        csv_row = [server_name, server_ip, server_os, package_name, patch_run, status, current_date, comment]
        row.append(csv_row)
        email_send_patching_failed(server_ip, msg)
    else:
        updates = res["data"]["updates"]
        if updates:
            for update in updates:
                server_name = res["server_name"]
                server_ip = res["ip"]
                server_os = res["os_distribution"]
                package_name = 'KB'+updates[update]['kb'][0]
                patch_run = res["patch_run"]
                status = "Successful"
                comment = updates[update]['title']

                csv_row = [server_name, server_ip, server_os, package_name, patch_run, status, current_date, comment]

                row.append(csv_row)
        else:
            if res["patch_run"] == '1':    
                server_name = res["server_name"]
                server_ip = res["ip"]
                server_os = res["os_distribution"]
                package_name = "-"
                patch_run = res["patch_run"]
                status = "-"
                comment = "No updates available"

                csv_row = [server_name, server_ip, server_os, package_name, patch_run, status, current_date, comment]

                row.append(csv_row)     
        
    # print(row)


fields = ['Server Name', 'Server IP', 'OS Distribution', 'Package Name', 'Patch Run', 'Status', 'Date', 'Comment']
date = datetime.datetime.now()
filename = date.strftime("%m_%d_%Y_%H_%M_%S") + "_windows_report_new.csv"

with open(filename, 'w') as csvfile:
# creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(row)
    print('CSV created with name: ' + filename)
