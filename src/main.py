import os

from lxml import etree as ET

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


parser = ET.XMLParser(strip_cdata=False, remove_blank_text=True)

for file in os.listdir(ROOT_DIR):
    if file.endswith('.xml') or file.endswith('.XML'):
        with open(file, 'r+', encoding="utf8") as data:
            parserino = ET.parse(data, parser=parser).getroot()

            form1Xml = ET.XML('<Form FileID="PrimitivePersonalNumberInput" index="1" id="PersonalNumberInput"  /> ')
            form2Xml = ET.XML('<Form FileID="PrimitiveChoosePhone" index="2" id="ChoosePhone" />')
            form3Xml = ET.XML('<Form FileID="PrimitiveOTP" index="3" id="OTP" />')
            idForm = ET.XML('''  <Identification>
    <PersonalNumberForm>
      <InputFields>
        <Field name="personalnumber" length="11" fieldMask="^[0-9]{11}$" fieldFlags="73" sortIndex="1" type="MobileNumber" />
      </InputFields>
      <TimeOut>60000</TimeOut>
    </PersonalNumberForm>
    <PrimitiveChoosePhone>
      <PerPage>3</PerPage>
      <CellWidth>430</CellWidth>
      <TimeOut>60000</TimeOut>
    </PrimitiveChoosePhone>
    <PrimitiveOTP>
      <InputFields>
        <Field name="OTP" length="4" fieldMask="^[0-9]{4}$" fieldFlags="73" value=""  sortIndex="1" type="MobileNumber" />
      </InputFields>
      <TimeOut>60000</TimeOut>
      <SubmitTriesLimit>3</SubmitTriesLimit>
      <ResendSMSLimit>3</ResendSMSLimit>
      <ResendTimeOut>5000</ResendTimeOut>
      <SuccessTimeOut>5000</SuccessTimeOut>
      <FailedTimeOut>5000</FailedTimeOut>
    </PrimitiveOTP>
  </Identification>''')

            et = ET.ElementTree(parserino)

            for x in parserino.xpath('//Form'):
                x.attrib['index'] = (str(int(x.attrib['index']) + 3))

            for x in parserino.xpath('//Forms'):
                x.insert(0, form3Xml)
                x.insert(0, form2Xml)
                x.insert(0, form1Xml)

            checkTemplate = parserino.find(".//PrintedCheckTemplate")
            idRoot = checkTemplate.getparent()
            idRoot.insert(idRoot.index(checkTemplate) + 3, idForm)

            if parserino.tag == "PrimitivePayment":
                parserino.tag = "PrimitivePaymentIdentification"

            elif parserino.tag == "ComplexPayment":
                parserino.tag = 'ComplexPaymentIdentification'



            et.write(file, encoding='utf-8', pretty_print=True, xml_declaration=True)
            print("%s Got Identified" % file)
