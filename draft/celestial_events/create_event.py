from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)




#this is static - need to make it dynamic to account for each event
    event_request_body = {
        'start' : {
            'date' : '2020-11-15'
        },
        'end' : {
            'date' : '2020-11-16'
        },
        'summary' : 'new moon',
        'description' : 'description here',
        'colorId' : 8,
        'status' : 'confirmed',
        'transparency' : 'opaque',
        'visibility' : 'public',
        'location' : 'Toronto, ON'
    }

    response = service.events().insert(
        calendarId = 'primary',
        body = event_request_body
    ).execute()

if __name__ == '__main__':
    main()
    
