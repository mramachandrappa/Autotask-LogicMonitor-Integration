#!/bin/env python

FieldName = 'TicketType'
FieldValue = '3'
AccountID = '337'
AT_IntegrationCode = '<IntegrationCode>'

def Ticket_Query():
    reqBody = """<?xml version="1.0" encoding="UTF-8"?>
      <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soap:Header>
          <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
            <IntegrationCode>AT_IntegrationCode</IntegrationCode>
         </AutotaskIntegrations>
   </soap:Header>
   <soap:Body>
      <query xmlns="http://autotask.net/ATWS/v1_6/">
         <sXML><![CDATA[<queryxml>
         <entity>Ticket</entity>
         <query>
         <condition><field>fieldName<expression op="equals">fieldValue</expression></field></condition>
         <condition><field>Status<expression op="notequal">5</expression></field></condition>
         <condition><field>AccountID<expression op="equals">accountName</expression></field></condition>
         </query>
         </queryxml>]]></sXML>
      </query>
   </soap:Body>
   </soap:Envelope>"""

    body = reqBody.replace('AT_IntegrationCode', AT_IntegrationCode).replace('fieldName', FieldName).replace('fieldValue', FieldValue).replace('accountName', AccountID)

    return (body)

def Installed_Product_Query():
    reqBody = """<?xml version="1.0" encoding="UTF-8"?>
      <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soap:Header>
          <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
            <IntegrationCode>AT_IntegrationCode</IntegrationCode>
         </AutotaskIntegrations>
   </soap:Header>
   <soap:Body>
      <query xmlns="http://autotask.net/ATWS/v1_6/">
         <sXML><![CDATA[<queryxml>
         <entity>InstalledProduct</entity>
         <query>
         Installed_Product_Query
         <condition><field>AccountID<expression op="equals">AccountName</expression></field></condition>
         </query>
         </queryxml>]]></sXML>
      </query>
   </soap:Body>
   </soap:Envelope>"""
    body = reqBody.replace('AT_IntegrationCode', AT_IntegrationCode).replace('AccountName', AccountID)
    return (body)

def Product_Query():
    reqBody = """<?xml version="1.0" encoding="UTF-8"?>
      <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soap:Header>
          <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
            <IntegrationCode>AT_IntegrationCode</IntegrationCode>
         </AutotaskIntegrations>
   </soap:Header>
   <soap:Body>
      <query xmlns="http://autotask.net/ATWS/v1_6/">
         <sXML><![CDATA[<queryxml><entity>Product</entity>
         <query>Product_Query</query>
         </queryxml>]]></sXML>
      </query>
   </soap:Body>
   </soap:Envelope>"""

    body = reqBody.replace('AT_IntegrationCode', AT_IntegrationCode)

    return (body)