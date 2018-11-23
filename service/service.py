import csv
import requests
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Let's do it with Google Drive API because it 
# allows us to create a sheet from CSV file
# without updating cells row-by-row
scope = 'https://www.googleapis.com/auth/drive'

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', scope)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))
file_metadata = {
    'name': 'Server Status Report',
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

# Please notice that we do this like that - authorize ourselves with Drive API
# before getting the hands on the file with a list because in case of a big file
# (I mean, 10000 links and more) we will totally want to decrease usage of the memory.
# So let's store it for short time, okay?)

# get a list of links from the file and store it in the variable
file = open('path_to_file.txt', 'rt')
initial_list = file.read()
file.close()

# >> ["link", "link"]
list_of_links = initial_list.split('\n')

# create a new file for a list of links with responses
responses_list = open('responses_list.txt', 'wt')

# treat the responses_list as CSV file and
# write links along with status codes with a comma delimiter row-by-row
with responses_list as csvfile:
    file_writer = csv.writer(csvfile, 
                             delimiter = ',')
    for link in list_of_links:
        request = requests.get(link, allow_redirects = False)
        file_writer.writerow([link, request.status_code])

# upload our file using Drive API...
media = MediaFileUpload('responses_list.csv',
                        mimetype='text/csv',
                        resumable=True)

# ... and close the list for good
responses_list.close()

# create the sheet
sheet = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

print 'File ID: %s' % sheet.get('id')
