#import libraries
from gazpacho import get, Soup
import pandas as pd
import numpy as np
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re


#webscraping
url = 'https://www.timeanddate.com/astronomy/sights-to-see.html'
html = get(url)
soup = Soup(html)

#from article class tag
rows = soup.find('article', {'class' : 'post-row'})
row = rows[11]
row
date = row.find('h3').text
date

titles = row.find('a')
title = titles[0].text
title
print(type(title))

descriptions = row.find('p')
descriptions
#description = descriptions[0].text
print(type(descriptions))


def parser():
    rows = soup.find('article', {'class' : 'post-row'})

    dates = []
    title_list = []
    description_list = []

    for row in rows:
        date = row.find('h3').text
        dates.append(date)

        titles = row.find('a')
        title = titles[0].text
        title_list.append(title)

        descriptions = row.find('p')
        #description = descriptions[0]
        #print(description)
        description_list.append(descriptions)

    return dates, title_list, description_list

output = parser()

#data cleaning
df = pd.DataFrame(output).T
df.head()
df=df.rename(columns={0: 'date', 1: 'event', 2: 'description'})
df.info()
df['start_year'] = '2021'
df.head()

df.iloc[0:10, 3] = '2020'
df.iloc[38, 1] = 'Draconid Meteor Shower'
df.iloc[39, 1] = 'Orionid Meteor Shower'
df.iloc[-2, 1] = 'Micro Full Moon'
df.iloc[-1, 1] = 'Super New Moon'
df.tail()
df.info()

#date format needed for google calendar API:
# "2015-06-01"

#to get month
def month_generator(date_month_day_or_days):
    month = []
    for s in date_month_day_or_days:
        if 'Jan' in date_month_day_or_days:
            month = '01'
        elif 'Feb' in date_month_day_or_days:
            month = '02'
        elif 'Mar' in date_month_day_or_days:
            month = '03'
        elif 'Apr' in date_month_day_or_days:
            month = '04'
        elif 'May' in date_month_day_or_days:
            month = '05'
        elif 'Jun' in date_month_day_or_days:
            month = '06'
        elif 'Jul' in date_month_day_or_days:
            month = '07'
        elif 'Aug' in date_month_day_or_days:
            month = '08'
        elif 'Sep' in date_month_day_or_days:
            month = '09'
        elif 'Oct' in date_month_day_or_days:
            month = '10'
        elif 'Nov' in date_month_day_or_days:
            month = '11'
        elif 'Dec' in date_month_day_or_days:
            month = '12'
    return month

#to get dates
def find_days(string):
    days = [int(s) for s in re.findall(r'\b\d+\b', string)]
    return days

def start_date(day_list):
    len_list = len(day_list)
    if len_list == 2:
        date_start = day_list[0]
    elif len_list == 1:
        date_start = day_list[0]
    return date_start

def end_date(day_list):
    len_list = len(day_list)
    if len_list == 2:
        date_end = day_list[1]
    elif len_list == 1:
        date_end = day_list[0]
    return date_end

def to_str(text):
    for i in df:
        try:
            text = ''.join([str(elem) for elem in text])
        except: TypeError
        return text

def remove_tags(text):
    try:
        text = text.replace('<p>', '').replace('</p>', '').replace('<p class="large-link">', '')
    except: AttributeError
    return text
#remove_tags(ret)
#tester = df['description'][2]
#tester_str = ''.join([str(elem) for elem in tester])
#print(type(tester_str))
#remove_tags(tester_str)

#apply functions to df to clean up date
df['desc_str'] = df['description'].apply(lambda x: to_str(x))
df['desc_no_tags'] = df['desc_str'].apply(lambda x: remove_tags(x))

df.iloc[9, 5] = 'At 13:50 UTC, the Earth will reach its perihelion—the point on its orbit that is closest to the Sun.'
df.iloc[11, 5] = 'The Moon will come between the Sun and the Earth, and the illuminated side of the Moon will face away from the Earth. A New Moon is almost impossible to see, even with a telescope.'
df.iloc[14, 5] = 'February\'s Full Moon is also known as Snow Moon in many Northern Hemisphere cultures.'
df.iloc[15, 5] = 'Dark nights a few days before and after the Moon reaches its New Moon phase at 10:21 UTC on March 13 are the best nights to do some night sky watching.'
df.iloc[17, 5] = 'March 2021\'s Super Full Moon is also the Worm Moon, named after earthworms that tend to appear around in this time in many locations in the Northern Hemisphere.'
df.iloc[20 ,5] = 'The Full Moon in April is sometimes known as the Pink Moon because of phlox, a pink flower, that blooms around this time in the North.'
df.iloc[21, 5] = 'April\'s Pink Full Moon is also a Super Moon. Because the Full Moon takes place when the Moon is at its perigee, it will look a little larger than a usual Full Moon.'
df.iloc[24, 5] = 'This year\'s Full Moon in May, also known as the Flower Moon after all the flowers that bloom around this time in the Northern Hemisphere, is a Super Moon. It may look bigger and brighter compared to other Full Moons.'
df.iloc[29, 5] = 'June\'s Full Moon is often called the Strawberry Full Moon, after the berries that grow in the Northern Hemisphere around this time of the year.'
df.iloc[31, 5] = 'July\'s Full Moon is also known as Thunder Moon, Hay Moon, and Wort Moon.'
df.iloc[35, 5] = 'A New Moon in the sky means no moonlight to hinder your view of stars and planets. Use the Interactive Night Sky Map to find out what planets are visible tonight and where.'
df.iloc[40, 5] = 'This New Moon takes place very close to its perigee—the point on its orbit closest to the Earth.'
df.iloc[41, 5] = 'The 2021 November Full Moon is a Micromoon—it occurs when the Moon is closest to its apogee.'
df.iloc[42, 5] = 'This New Moon takes place very close to its perigee—the point on its orbit closest to the Earth.'

df.tail(25)

df['start_month'] = df['date'].apply(lambda x: month_generator(x))
df['day_list'] = df['date'].apply(lambda x: find_days(x))
df['start_day'] = df['day_list'].apply(lambda x: start_date(x))
df['start_day'] = df['start_day'].astype(str)

df['end_year'] = df['start_year']
df['end_month'] = df['date'].apply(lambda x: month_generator(x))
df['end_day'] = df['day_list'].apply(lambda x: end_date(x))
df['end_day'] = df['end_day'].astype(str)
df.columns

#df = df.drop(['date', 'day_list', 'start_year', 'desc_str', 'start_month', 'start_day', ], axis=1)
df.info()

df['start_date']= df['start_year'] + '-' + df['start_month'] + '-' + df['start_day']
df['end_date'] = df['end_year'] + '-' + df['end_month'] + '-' + df['end_day']
df.columns
df = df.drop(['date', 'start_year', 'desc_str', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day'], axis=1)

df.head(45)


#access first row [0], all columns [:]
df.iloc[0, :]

#access data required for google calendar api event, first row



#connecting with google calendar api
len_df = len(df)
print(len_df)
i = 0

while i <= len_df:
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

        # create a new calendar
        # calendar = {
        #     'summary' : 'Space Dates',
        #     'timeZone': 'America/New_York'
        #  }

        #created_calendar = service.calendars().insert(body=calendar).execute()

        #this is static - need to make it dynamic to account for each event

        event_name = df.iloc[i, 1]
        description = df.iloc[i, 2]
        start_date = df.iloc[i, -2]
        end_date = df.iloc[i, -1]

        event_request_body = {
            'start' : {
                'date' : start_date
            },
            'end' : {
                'date' : end_date
            },

            'summary' : event_name,
            'description' : description,
            'colorId' : 8,
            'status' : 'confirmed',
            'transparency' : 'transparent',
            'visibility' : 'private',
            'location' : 'Toronto, ON',
            'attendees' : [
                {
                    'displayName' : 'Melissa Griffin',
                    'email' : 'melissa.c.griffin@gmail.com'
                }
            ]
        }

        #sendNotification = True,

        response = service.events().insert(
            calendarId = 'Space Dates',
            #sendNotification = 'sendNotification',
            body = event_request_body
        ).execute()

    if __name__ == '__main__':
        main()
