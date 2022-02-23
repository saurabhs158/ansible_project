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
    #print(res)
    user_data = res["data"]["stdout_lines"]
    for users in user_data:
        data = users
        data = data.split(":")
        del data[1:3]
        data_count = len(data)
        row_count = 1
        for d in range(data_count):
            if row_count < data_count:
               #print(d)
               if data[row_count] != '':
                  csv_row = [data[0], data[row_count]]
                  row.append(csv_row)
                  row_count += 1
                
date = datetime.datetime.now()
filename = date.strftime("%m_%d_%Y_%H_%M_%S") + "_linux_user_audit.csv"
fields = ['Group Name', 'User name']

with open(filename, 'w') as csvfile:
# creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the data rows
    csvwriter.writerow(fields)
    csvwriter.writerows(row)
    print('CSV created with name: ' + filename)
