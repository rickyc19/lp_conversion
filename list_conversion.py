import pygsheets
import phonenumbers
from urlextract import URLExtract
import pyap
import os

client = pygsheets.authorize(client_secret='oauth.json')
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CIpWBZXAK_PqsEq2vLlFklT2MgQjH008qbxgPYXbRtU/edit#gid=0")
sheet = spreadsheet.sheet1

cells = sheet.get_col(1, include_tailing_empty=False, returnas='cells')
phone_string = ""
web_string = ""
add_match = ""
add_string = ""

data_matrix = [[]]
data_matrix.clear()
value_list = list()

# Add cell values to list
for c in cells:
    v = c.value
    value_list.append(v)

for l in value_list:

    try: add_string = pyap.parse(l, country='US')[0].__str__()  # Get address from list value
    except: add_string = ""

    try: web_string = URLExtract().find_urls(l)[0]  # Get URL from list value
    except: web_string = ""

    for match in phonenumbers.PhoneNumberMatcher(l, "US"):  # Get phone number from list value
        phone_string = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)

    # Add data to matrix
    data_matrix.append([phone_string, web_string, add_string])
    phone_string = ""

sheet.update_values("B:D", data_matrix)  # Update cell range

