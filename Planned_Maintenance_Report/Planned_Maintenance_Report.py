#!/bin/env python

import requests
import csv
from xml.dom import minidom
import datetime
from update_widget import update_widget

selectField = "TicketType"
selectStatus = "4" #Change Request
AccountID = "337" #Clarus

url = 'https://webservices4.autotask.net/ATServices/1.6/atws.asmx'
headers = {'content-type': 'text/xml'}
uri = 'https://ww4.autotask.net/Mvc/ServiceDesk/TicketDetail.mvc?ticketId=urlid'
href_link = '<a href=link target=_blank>tickets</a>'

#SOAP query returns all Change Request type Tickets with all status except "Complete"
reqBody ="""<?xml version="1.0" encoding="UTF-8"?>
      <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soap:Header>
          <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
            <IntegrationCode><AT_Auth_Code></IntegrationCode>
         </AutotaskIntegrations>
   </soap:Header>
   <soap:Body>
      <query xmlns="http://autotask.net/ATWS/v1_6/">
         <sXML><![CDATA[<queryxml><entity>Ticket</entity><query><condition><field>fieldName<expression op="equals">statusCode</expression></field></condition><condition><field>Status<expression op="notequal">5</expression></field></condition><condition><field>AccountID<expression op="equals">AccountName</expression></field></condition></query></queryxml>]]></sXML>
      </query>
   </soap:Body>
   </soap:Envelope>"""


#Replacing params based on user inupt
body = reqBody.replace("statusCode", selectStatus).replace("fieldName", selectField).replace("AccountName", AccountID)

auth_values = ('<Username>', '<Password>')
    
response = requests.post(url, data=body, headers=headers, auth=auth_values)

str1 = response.content

print (str1)

with open('data.xml', 'wb+') as f:
      f.write(str1)

doc = minidom.parse('data.xml')

statusList = []
ticketStatuses = doc.getElementsByTagName('Status')
for ticketStatus in ticketStatuses:
  if ticketStatus.firstChild.data == "17":
     ticketStatus.firstChild.data = "On Hold"
  elif ticketStatus.firstChild.data == "23":
       ticketStatus.firstChild.data = "Waiting Customer Inputs"
  elif ticketStatus.firstChild.data == "13":
       ticketStatus.firstChild.data = "Waiting for Approval"
  elif ticketStatus.firstChild.data == "22":
       ticketStatus.firstChild.data = "First Response Initiated"
  elif ticketStatus.firstChild.data == "1":
       ticketStatus.firstChild.data = "New"
  elif ticketStatus.firstChild.data == "8":
       ticketStatus.firstChild.data = "In Progress"
  elif ticketStatus.firstChild.data == "21":
       ticketStatus.firstChild.data = "Scheduled"
  elif ticketStatus.firstChild.data == "24":
       ticketStatus.firstChild.data = "Resolved/Closure Confirm"
  elif ticketStatus.firstChild.data == "5":
       ticketStatus.firstChild.data = "Complete"
  elif ticketStatus.firstChild.data == "26":
       ticketStatus.firstChild.data = "Action Required"
  elif ticketStatus.firstChild.data == "12":
       ticketStatus.firstChild.data = "Waiting Vendor Inputs"
  elif ticketStatus.firstChild.data == "7":
       ticketStatus.firstChild.data = "Waiting Customer"
  statusList.append(ticketStatus.firstChild.data)

ticketList = []
ticketNumbers = doc.getElementsByTagName('TicketNumber')
for ticketNumber in ticketNumbers:
    ticketList.append(ticketNumber.firstChild.data)
        
titleList = []
ticketTitles = doc.getElementsByTagName('Title')
for titleText in ticketTitles:
    titleList.append(titleText.firstChild.data)

start_Time = []
start_Time_1 = []
startTime = doc.getElementsByTagName('DueDateTime')
for date in startTime:
    start_Time.append((date.firstChild.data).replace("T", " "))
    start_Time_1.append(str(date.firstChild.data).replace("T", " ") + " CEST")

for m in range(len(start_Time)):
    if "." not in start_Time[m]:
        start_Time[m] = start_Time[m].__add__(".00")

Duration = []
Duration_1 = []
entities = doc.getElementsByTagName('Entity')
for e in entities:
    if e.getElementsByTagName("EstimatedHours"):
        Duration.append(int(float(e.getElementsByTagName('EstimatedHours')[0].firstChild.data)))
        Duration_1.append(str(int(float(e.getElementsByTagName('EstimatedHours')[0].firstChild.data))) + "h")
    else:
        Duration.append(int(0))
        Duration_1.append("0" + "h")
  
End_Time = []
for a, e in zip(start_Time, Duration):
    End_Time.append(str(datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(hours=e)) + " CEST")

idList = []
ticketIds = doc.getElementsByTagName('id')
for urlId in ticketIds:
    idList.append(urlId.firstChild.data)

equipmentList = []
eqLists = doc.getElementsByTagName('ChangeInfoField1')
for eqList in eqLists:
    try:
        equipmentList.append(eqList.firstChild.data)
    except AttributeError:
        equipmentList.append("No data")
        continue

TypeOfWork = []
TOWork = doc.getElementsByTagName('ChangeInfoField2')
for work in TOWork:
    try:
        TypeOfWork.append(work.firstChild.data)
    except AttributeError:
        TypeOfWork.append("No data")
        continue

ImpactOfWork = []
EOWork = doc.getElementsByTagName('ChangeInfoField3')
for work in EOWork:
    try:
        ImpactOfWork.append(work.firstChild.data)
    except AttributeError:
        ImpactOfWork.append("No data")
        continue

ImpactedSystems = []
ImpactedSystem = doc.getElementsByTagName('ChangeInfoField4')
for IS in ImpactedSystem:
    try:
        ImpactedSystems.append(IS.firstChild.data)
    except AttributeError:
        ImpactedSystems.append("No data")
        continue

loc_of_work = []
location = doc.getElementsByTagName('ChangeInfoField5')
for note in location:
    try:
        loc_of_work.append(note.firstChild.data)
    except AttributeError:
        loc_of_work.append("No data")
        continue

urlList = []
for i in range(len(idList)):
  htmlUrl= uri.replace("urlid", idList[i]) 
  urlList.append(htmlUrl)

ticket_urls =[]
for t in range(len(ticketList)):
  ticket_url = href_link.replace("link", urlList[t]).replace("tickets",ticketList[t])
  ticket_urls.append(ticket_url)

data=zip(ticket_urls, statusList, start_Time_1, Duration_1, End_Time, equipmentList, TypeOfWork, ImpactOfWork, ImpactedSystems, loc_of_work, titleList)

def csv_content():
  csv_reader = []
  try:
    with open('ChangeRequest.csv', 'r') as infile:
      reader = csv.reader(infile)
      for i in reader:
        csv_reader.append(i)
      infile.close()
    return csv_reader
  except IOError:
    print ("No file exist as ChangeRequest.csv")
    pass

#Reading contents of already existed csv file
csv_reader = csv_content()

with open('ChangeRequest.csv', 'w', newline='') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(("Ticket Number", "Status", "Start Time", "Duration", "Estimated End Time", "Equipment", "Type of Work", "Impact of Work", "Impacted System", "Location of Work", "Titles"))
    for row in data:
        writer.writerow(row)
    myfile.close()

#Reading contents of csv file after updating with changes if any.
csv_writer = csv_content()

#If change in contents of file, update the widget.
if csv_reader != csv_writer:
  print ("Change in contents of file")
  update_widget()
else:
  print ("No change in file")
