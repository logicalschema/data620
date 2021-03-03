import xml.etree.ElementTree as ET
import pandas as pd 
  


''' Sample XML Member Node
<member>
        <member_full>Barrasso (R-WY)</member_full>
        <last_name>Barrasso</last_name>
        <first_name>John</first_name>
        <party>R</party>
        <state>WY</state>
        <address>307 Dirksen Senate Office Building Washington DC 20510</address>
        <phone>(202) 224-6441</phone>
        <email>https://www.barrasso.senate.gov/public/index.cfm/contact-form</email>
        <website>http://www.barrasso.senate.gov</website>
        <class>Class I</class>
        <bioguide_id>B001261</bioguide_id>
</member>
'''

# Parsing the XML file: https://www.senate.gov/general/contact_information/senators_cfm.xml
tree = ET.parse('senators.xml')
root = tree.getroot()

# Declaration of fields we will be interested in
cols = ["first_name", "last_name", "party", "state"]
rows = []


for senator in tree.iter('member'):
    temp = {}
    for key in cols:
        temp[key] = senator.find(key).text

    rows.append(temp)

df = pd.DataFrame(rows, columns = cols)


print(df)    

# Writing dataframe to csv 
df.to_csv('output.csv') 