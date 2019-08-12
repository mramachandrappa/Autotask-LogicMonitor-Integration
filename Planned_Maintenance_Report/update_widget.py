#!/bin/env python

import requests
import json
import hashlib
import base64
import time
import hmac
import json
import sys

def update_widget():
  filein = open('ChangeRequest.csv', "r")
  fileout = open("html-table.html", "w")
  data = filein.readlines()

  table = """
    <html>
     <head>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
        <style>
          .table-bordered{margin-bottom: 30px;}
          th{background-color: rgb(1, 118, 255); color: #ffffff;}
          thead th { position: sticky; top: -1; }
          .table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th {
          padding: 8px;line-height: 2.428571;vertical-align: top; 
          border-top: 2px solid #ddd; font-size: 14px; 
          font-family: Trebuchet MS}
        </style>
     </head>
    <body>
     <table class="table table-striped">
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

  fileout.writelines(table)
  fileout.close()
  filein.close()

#Account Info
  AccessId ='<AccessId>'
  AccessKey ='<AccessKey>'
  Company = '<api>'

  #Request Info
  httpVerb ='PUT'
  resourcePath = '/dashboard/widgets/<widgetID>'
  queryParams =''

  dict = {"name":"Planned Maintenance","dashboardId":<dashboardID>, "type":"text", "theme" : "borderBlue"}
  dict['content'] = html_source
  data=json.dumps(dict)

  #Construct URL
  url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams

  #Get current time in milliseconds
  epoch = str(int(time.time() * 1000))

  #Concatenate Request details
  requestVars = httpVerb + epoch + data + resourcePath

  #Construct signature
  my_hmac = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
  signature = base64.b64encode(my_hmac.encode())

  #Construct headers
  auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
  headers = {'Content-Type':'application/json','Authorization':auth}

  #Make request
  response = requests.put(url, data=data, headers=headers)

  #Print status and body of response
  print ('Response Status:',response.status_code)
  print ('Response Body:',response.content)
