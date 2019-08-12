#!/usr/bin/python
import requests
import csv
from xml.dom import minidom
from update_widget import update_widget

#From Autotask Accounts.
AccountID = '337'

url = 'https://webservices4.autotask.net/ATServices/1.6/atws.asmx'
headers = {'content-type': 'text/xml'}
uri = 'https://ww4.autotask.net/Mvc/ServiceDesk/TicketDetail.mvc?ticketId=urlid'
href_link = '<a href=link target=_blank>tickets</a>'
condition = '<condition><field>AccountID<expression op="equals">AccountName</expression></field></condition>'
reqBody = """<?xml version="1.0" encoding="UTF-8"?>
      <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soap:Header>
          <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
            <IntegrationCode><Integration Code></IntegrationCode> 
         </AutotaskIntegrations>
   </soap:Header>
   <soap:Body>
      <query xmlns="http://autotask.net/ATWS/v1_6/">
         <sXML><![CDATA[<queryxml><entity>Contact</entity><query>conditions_list</query></queryxml>]]></sXML>
      </query>
   </soap:Body>
   </soap:Envelope>"""

# Replacing params
body = reqBody.replace('conditions_list', condition).replace('AccountName', AccountID)

auth_values = ('<username>','<Password>')

response = requests.post(url, data=body, headers=headers, auth=auth_values)
with open('data.xml', 'wb+') as f:
    f.write(response.content)

doc = minidom.parse('data.xml')

UserFields = doc.getElementsByTagName('UserDefinedFields')
Entity = doc.getElementsByTagName('Entity')
id_list = []
for i, e in zip(UserFields, Entity):
    if i.getElementsByTagName('Value'):
        s = e.getElementsByTagName('id')
        for x in s:
            id_list.append(x.firstChild.data)
print(id_list)

condition += '<condition><field>id<expression op="equals">values_list</expression></field></condition>'
fields_list = []
for a in range(len(id_list)):
    c = condition.replace('values_list', id_list[a]).replace('AccountName', AccountID)
    fields_list.append(c)

Contact_Name = []
Email = []
Phone = []
MobilePhone = []
Level = []

for fields in fields_list:
    a = reqBody.replace('conditions_list', fields)
    response = requests.post(url, data=a, headers=headers, auth=auth_values)
    with open('data.xml', 'wb+') as f:
        f.write(response.content)
    doc = minidom.parse('data.xml')
    Entity = doc.getElementsByTagName('Entity')
    for name in Entity:
        if name.getElementsByTagName('FirstName') and name.getElementsByTagName('LastName'):
            Contact_Name.append(name.getElementsByTagName('FirstName')[0].firstChild.data + " " + name.getElementsByTagName('LastName')[0].firstChild.data)
        else:
            Contact_Name.append(N/A)
    for elements in Entity:
        if elements.getElementsByTagName('EMailAddress'):
            Email.append(elements.getElementsByTagName('EMailAddress')[0].firstChild.data)
        else:
            Email.append("N/A")
    for number in Entity:
        if number.getElementsByTagName('Phone'):
            try:
                Phone.append(number.getElementsByTagName('Phone')[0].firstChild.data)
            except AttributeError:
                Phone.append("N/A")
        else:
            Phone.append("N/A")
    for mobile in Entity:
        if mobile.getElementsByTagName('MobilePhone'):
            try:
                MobilePhone.append(mobile.getElementsByTagName('MobilePhone')[0].firstChild.data)
            except AttributeError:
                MobilePhone.append('N/A')
        else:
            MobilePhone.append("N/A")
    UserFields = doc.getElementsByTagName('UserDefinedField')
    for esc_level in UserFields:
        if esc_level.getElementsByTagName('Value'):
            Level.append(esc_level.getElementsByTagName('Value')[0].firstChild.data)
        else:
            Level.append("N/A")

Level_1 = Level[1::2]

print(Contact_Name)
print(Email)
print(Phone)
print(MobilePhone)
print(Level)
print (Level_1)

data = zip(Contact_Name, Email, Phone, MobilePhone, Level_1)
data1 = sorted(data, key = lambda x: x[4])

#Checking if Contacts.csv file already exists and read the content of it before writing new data.
def csv_content():
  csv_reader = []
  try:
    with open('Contacts.csv', 'r') as infile:
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

with open('Contacts.csv', 'w', newline='') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(("Point of Contact", "Email ID", "Phone", "Mobile Phone", "Escalation Level"))
    for row in data1:
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
