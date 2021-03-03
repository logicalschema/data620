import xml.etree.ElementTree as ET
import pandas as pd 
from bs4 import BeautifulSoup
import requests
  


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

senatorsDF = pd.DataFrame(rows, columns = cols)  



# This section gets the Social Media information for senators
# url="https://triagecancer.org/congressional-social-media"

# This url was used 
url = "https://raw.githubusercontent.com/logicalschema/data620/main/Project%201/data/social-media.html"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")

tables = soup.findChildren('table')
rep_table = tables[0]
rows = rep_table.find_all(['tr'])

# Each <tr> in the table has these fields
''' Sample tr
    <tr data-row_id="0" class="ninja_table_row_0 nt_row_id_0">
        <td>Alabama</td>
        <td>U.S. Senator</td>
        <td>Shelby, Richard</td>
        <td>https://www.shelby.senate.gov/public/</td>
        <td>R</td>
        <td>@SenShelby</td>
        <td>https://twitter.com/SenShelby?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor</td>
        <td>@senatorshelby</td>
        <td>https://www.instagram.com/senatorshelby/</td>
        <td>x</td>
        <td>https://www.facebook.com/RichardShelby</td>
    </tr>
'''
rep_colnames = ['State', 'Status', 'Name', 'NameLink', 'Party', 'Twitter', 'TwitterLink', 'Instagram', 'InstagramLink', 'Facebook', 'FacebookLink']

reps = []

#Omitting the 1st row because it is the header row
for row in rows[1::]:

    temp = {}
    temp_names = rep_colnames.copy()
    cells = row.findChildren('td')

    for cell in cells:
      #value = cell.string
      temp[temp_names.pop(0)] = cell.string

    reps.append(temp)

# Convert the list of representatives to a dataframe
df = pd.DataFrame(reps, columns = rep_colnames)

# We will only export the U.S Senators
senatorInfo =  df[df['Status'] == 'U.S. Senator']



# The following dictionary is for converting States to their two letter abbreviation
# Courtesy of https://gist.github.com/rogerallen/1583593
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}



'''
senatorsDF
cols = ["first_name", "last_name", "party", "state"]

senatorInfo
rep_colnames = ['State', 'Status', 'Name', 'NameLink', 'Party', 'Twitter', 'TwitterLink', 'Instagram', 'InstagramLink', 'Facebook', 'FacebookLink']

'''

verify = pd.DataFrame(columns = rep_colnames)
count = 0
for i in senatorsDF.index:

    first_name = senatorsDF['first_name'][i]
    last_name = senatorsDF['last_name'][i]
    party = senatorsDF['party'][i]
    stateAbbreviation = senatorsDF['state'][i]
    state = list(us_state_abbrev.keys())[list(us_state_abbrev.values()).index(stateAbbreviation)]


    temp = senatorInfo[ (senatorInfo['State'] == state) & (senatorInfo['Party'] == party) & (senatorInfo['Name'].str.contains(last_name)) ]
    index = temp.index
    if len(index) == 1:
        verify = pd.concat([verify, temp],  ignore_index=True)

    if len(index) < 1:
        print(last_name + ", " + first_name + " of " + state + " and member of " + party + " is missing.")


# Verify the senators with social media information
index = verify.index
if len(index) != 100:
    print("There are missing senators!")
else: 
    print("All senators are accounted for.")  


# At the time of this run 3/3/21, Catherine Cortez Masto (Nevada) and Tammy Duckworth (Illinois) are missing
# This section will add them in

cortez_masto = {'State': 'Nevada', 'Status': 'U.S. Senator', 'Name': 'Cortez Masto, Catherine', 'NameLink':'https://www.cortezmasto.senate.gov', 'Party': 'D', 'Twitter': '@SenCortezMasto', 'TwitterLink': 'https://twitter.com/sencortezmasto', 'Instagram': '@sencortezmasto', 'InstagramLink': 'https://www.instagram.com/sencortezmasto/', 'Facebook': 'x', 'FacebookLink':'https://www.facebook.com/SenatorCortezMasto/'}
duckworth = {'State': 'Illinois', 'Status': 'U.S. Senator', 'Name': 'Duckworth, Tammy', 'NameLink': 'https://www.duckworth.senate.gov/', 'Party': 'D', 'Twitter': '@SenDuckworth', 'TwitterLink': 'https://twitter.com/SenDuckworth', 'Instagram': '@senduckworth', 'InstagramLink': 'https://www.instagram.com/SenDuckworth/', 'Facebook': 'x', 'FacebookLink': 'https://www.facebook.com/SenDuckworth'}

verify = verify.append(cortez_masto, ignore_index=True)
verify = verify.append(duckworth, ignore_index=True)

verify.to_csv('Final_senators_social_media.csv') 