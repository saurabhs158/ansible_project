import sys
import json
import csv
import datetime
import smtplib
import ssl
import ast
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email_send_patching_failed(server_ip, error_msg):
    # sender_email = "#Add SMTP Email here#"
    # password = "#Add SMTP Pass here#"
    # sender = '#Add Sender Email here#'
    # receivers = '#Add Receiver Email here#'
    # server = smtplib.SMTP('smtp.gmail.com:587')
    sender = 'sgsalt201@capitaland.com'
    receivers = ['saurabh.shirke@global.ntt']
    server = smtplib.SMTP('smtp.dc.capitaland.com')
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
        #server.login(sender_email, password)
        server.sendmail(sender, receivers, msg.as_string())
        print("Successfully sent email")
    except Exception as e:
        print(e)
    finally:
        server.quit()

date = datetime.datetime.now()
current_date = date.strftime("%m-%d-%Y %H:%M:%S")
file_date = date.strftime("%Y-%m-%d")
file_name = str(sys.argv[1])
file = open(file_name, 'r')

servers = file.readlines()
#x = json.loads(x[0])
row = []

for server in servers:
    data = server
    try:
        res = ast.literal_eval(data)
    except:
        res = json.loads(data)

    if "unreachable" in res["data"]:
        server_name = res["server_name"]
        server_ip = res["ip"]
        server_os = res["os_distribution"]
        package_name = "-"
        status = "Failed"
        comment = res["data"]["msg"]
        msg = "Server " + server_name + "is unreachable. Patching failed. Error message:" + res["data"]["msg"]
        csv_row = [server_name, server_ip, server_os, package_name, status, current_date, comment]
        row.append(csv_row)
        
    elif res["data"]["failed"]:
        server_name = res["server_name"]
        server_ip = res["ip"]
        server_os = res["os_distribution"]
        package_name = "-"
        status = "Failed"
        comment = res["data"]["msg"]
        msg = "Server " + server_name + " patching failed. Error message:" + res["data"]["msg"]

        csv_row = [server_name, server_ip, server_os, package_name, status, current_date, comment]
        row.append(csv_row)
        email_send_patching_failed(server_ip, msg)
        
    elif res["data"]["stdout"] == 'No Updates':
        server_name = res["server_name"]
        server_ip = res["ip"]
        server_os = res["os_distribution"]
        package_name = "-"
        status = "-"
        comment = "No Updates Available"

        csv_row = [server_name, server_ip, server_os, package_name, status, current_date, comment]
        row.append(csv_row)

    else:
        packages = res["data"]["stdout_lines"]
        if packages:
            for package in packages:
                package = re.sub(' +', ',', package)
                package = package.split(',')
                package_name = package[0]
                server_name = res["server_name"]
                server_ip = res["ip"]
                server_os = res["os_distribution"]
                status = "Successful"
                comment = ""

                csv_row = [server_name, server_ip, server_os, package_name, status, current_date, comment]

                row.append(csv_row)
        else:
            package_name = "-"
            server_name = res["server_name"]
            server_ip = res["ip"]
            server_os = res["os_distribution"]
            status = "-"
            comment = "No Updates Available"

            csv_row = [server_name, server_ip, server_os, package_name, status, current_date, comment]

            row.append(csv_row)

fields = ['Server Name', 'Server IP', 'OS Distribution', 'Package Name', 'Status', 'Date', 'Comment']
date = datetime.datetime.now()
filename = date.strftime("%m_%d_%Y_%H_%M_%S") + "_linux_report_new.csv"


with open(filename, 'w') as csvfile:
# creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(row)
    print('CSV created with name: ' + filename)
