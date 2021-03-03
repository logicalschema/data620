from bs4 import BeautifulSoup
import requests
import pandas as pd 

url="https://triagecancer.org/congressional-social-media"

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

senatorInfo.to_csv('senator_socialmedia.csv') 