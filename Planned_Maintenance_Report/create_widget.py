#!/bin/env python

import requests
import json
import hashlib
import base64
import time
import hmac
import json
import sys

#HTML file creation
filein = open('ChangeRequest.csv', "r")
fileout = open("html-table.html", "w")
data = filein.readlines()

table = """<html>
<head>
<style>
#customers {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
  background-color: #4CAF50;
  color: white;
}
</style>
</head>
<body>
<h1 align="center"> Upcoming Planned Maintenances </h1>
<table class="table table-bordered inner-table" style="width: 100%">
<thead>
"""

# Create the table's column headers
header = data[0].split(",")

table += "<tr>\n"
for column in header:
    table += "<th>{0}</th>\n".format(column.strip())
table += "</tr>\n"
table +="</thead>\n"
table +="<tbody>\n"

# Create the table's row data
for line in data[1:]:
    row = line.split(",",10)
    table += "  <tr>\n"
    for column in row:
        table += "<td>{0}</td>\n".format(column.strip())
    table += "</tr>\n"

table += """</tbody>
            </table>
            </div>
            </body>
            </html>"""

html_source = str(table)

if "<tbody>\n<tr>" not in html_source:
  print ("no table content")

fileout.writelines(table)
fileout.close()
filein.close()

#Account Info
AccessId ='<AccessId>'
AccessKey ='<AccessKey>'
Company = '<api>'

#Request Info
httpVerb ='POST'
resourcePath = '/dashboard/widgets'
queryParams =''

dict = {"name":"Open S1 Tickets","dashboardId":<DashboardID>, "type":"text", "theme" : "borderBlue", "colSpan":10, "rowSpan":10}
dict['content'] = html_source
data=json.dumps(dict)

#Construct URL
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams

#Get current time in milliseconds
epoch = str(int(time.time() * 1000))

#Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath

#Construct signature
hmac = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
signature = base64.b64encode(hmac.encode())

#Construct headers
auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth}

#Make request
response = requests.post(url, data=data, headers=headers)

#Print status and body of response
print ('Response Status:',response.status_code)
print ('Response Body:',response.content)
