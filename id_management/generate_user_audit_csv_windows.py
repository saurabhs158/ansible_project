import json
import csv
import datetime
import smtplib
import ssl
import ast
import re
import sys

date = datetime.datetime.now()
current_date = date.strftime("%m-%d-%Y %H:%M:%S")
file_date = date.strftime("%Y_%m_%d_%H")
file_name = str(sys.argv[1])
file = open(file_name, 'r')

servers = file.readlines()
row = []

for server in servers:
    server = server.replace("/\/", "")

    try:
        res = ast.literal_eval(server)
    except:
        res = json.loads(server)

    user_data = res["data"]["stdout_lines"]
    for users in user_data:
        #print(users)
        data = users
        data = data.split(";")
        csv_row = []
        for d in data:
            #print(d)
            d = d.replace("\"","")
            csv_row.append(d)
        row.append(csv_row)
#print(row)
date = datetime.datetime.now()
filename = date.strftime("%m_%d_%Y_%H_%M_%S") + "_windows_user_audit.csv"

with open(filename, 'w') as csvfile:
# creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the data rows
    csvwriter.writerows(row)
    print('CSV created with name: ' + filename)
