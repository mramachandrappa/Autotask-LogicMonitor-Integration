#!/bin/env python

import requests
import csv
from xml.dom import minidom
import datetime
from update_widget import update_widget
from AT_Query import Installed_Product_Query, Ticket_Query, Product_Query

url = 'https://webservices4.autotask.net/ATServices/1.6/atws.asmx'
headers = {'content-type': 'text/xml'}
uri = 'https://ww4.autotask.net/Mvc/ServiceDesk/TicketDetail.mvc?ticketId=urlid'
href_link = '<a href=link target=_blank>tickets</a>'

#SOAP Query to fetch Ticket Data
Ticket_data = Ticket_Query()
auth_values = ('<username>', '<password>')

response = requests.post(url, data=Ticket_data, headers=headers, auth=auth_values)

str1 = response.content

with open('data.xml', 'wb+') as f:
      f.write(str1)

doc = minidom.parse('data.xml')

#Status of each Problem Ticket
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

#Ticket Numbers of all Problem Tickets.
ticketList = []
ticketNumbers = doc.getElementsByTagName('TicketNumber')
for ticketNumber in ticketNumbers:
    ticketList.append(ticketNumber.firstChild.data)

#Titles of all Problem Tickets
titleList = []
ticketTitles = doc.getElementsByTagName('Title')
for titleText in ticketTitles:
    titleList.append(titleText.firstChild.data)

#Creation date of all Problem Tickets.
CreationDate = []
ticket_date = doc.getElementsByTagName('CreateDate')
for i in ticket_date:
    CreationDate.append(str(datetime.datetime.strptime((i.firstChild.data).replace("T", " ")[:18], '%Y-%m-%d %H:%M:%S')) + " EST")

#Ticket ID's of all Problem Tickets.
idList = []
ticketIds = doc.getElementsByTagName('id')
for urlId in ticketIds:
    idList.append(urlId.firstChild.data)

#Adding Ticket ID's to the Ticket URL list.
urlList = []
for i in range(len(idList)):
  htmlUrl= uri.replace("urlid", idList[i])
  urlList.append(htmlUrl)

#Adding Ticket URL's to href_link
ticket_urls =[]
for t in range(len(ticketList)):
  ticket_url = href_link.replace("link", urlList[t]).replace("tickets",ticketList[t])
  ticket_urls.append(ticket_url)

#Fetching the Integer value of Config_Item from Problem Ticket.
Installed_Product_IDs = []
entities = doc.getElementsByTagName('Entity')
for e in entities:
    if e.getElementsByTagName('InstalledProductID'):
        Installed_Product_IDs.append(e.getElementsByTagName('InstalledProductID')[0].firstChild.data)
    else:
        Installed_Product_IDs.append('00000')

#Creating conditions list with each Installed_Product_ID.
fields = []
query = '<condition><field>id<expression op="equals">value</expression></field></condition>'
for a in range(len(Installed_Product_IDs)):
    b = query.replace('value', Installed_Product_IDs[a])
    fields.append(b)

#Querying Autotask with each condition fields to fetch ProductIDs.
IPQuery = Installed_Product_Query()
productID = []
for values in fields:
    a = IPQuery.replace("Installed_Product_Query", values)
    response = requests.post(url, data=a, headers=headers, auth=auth_values)
    with open('data.xml', 'wb+') as f:
        f.write(response.content)
    doc = minidom.parse('data.xml')
    product = doc.getElementsByTagName('EntityResults')
    for p in product:
        if p.getElementsByTagName('Entity'):
            a = p.getElementsByTagName('Entity')
            for i in a:
                if i.getElementsByTagName('ProductID'):
                    productID.append(i.getElementsByTagName('ProductID')[0].firstChild.data)
                else:
                    productID.append('00000')
        else:
            productID.append('00000')

#Creating Conditions list to query Autotask.
product_fields = []
product_query = '<condition><field>id<expression op="equals">value</expression></field></condition>'
for a in range(len(productID)):
    b = query.replace('value', productID[a])
    product_fields.append(b)

#Fetching Product Names by Querying PRODUCT Entity with product_fields.
PNQuery = Product_Query()
ProductName = []
for ids in product_fields:
    a = PNQuery.replace('Product_Query', ids)
    response = requests.post(url, data=a, headers=headers, auth=auth_values)
    with open('data.xml', 'wb+') as f:
        f.write(response.content)
    doc = minidom.parse('data.xml')
    product = doc.getElementsByTagName('EntityResults')
    for p in product:
        if p.getElementsByTagName('Entity'):
            a = p.getElementsByTagName('Entity')
            for i in a:
                if i.getElementsByTagName('Name'):
                    ProductName.append(i.getElementsByTagName('Name')[0].firstChild.data)
                else:
                    ProductName.append('None')
        else:
            ProductName.append('None')

data=zip(ticket_urls, statusList, CreationDate, ProductName, titleList)

#print (ticket_urls)
#print (statusList)
#print (CreationDate_1)
#print (ProductName)
#print (titleList)

#To check if ProblemTickets.csv file exists and read existed data.
def csv_content():
  csv_reader = []
  try:
    with open('ProblemTickets.csv', 'r') as infile:
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

#Create or Update ProblemTickets.csv with new data.
with open('ProblemTickets.csv', 'w', newline='') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(("Ticket Number", "Status", "Creation Date", "Configuration Item", "Titles"))
    for row in data:
        writer.writerow(row)
    myfile.close()

#Reading contents of csv file after updating with changes if any.
csv_writer = csv_content()

#Updating the widget based on Changes in csv.file
if csv_reader != csv_writer:
  print ("Change in contents of file -----> Updating the widget")
  update_widget()
else:
  print ("No change in file")