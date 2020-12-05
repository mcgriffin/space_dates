from gazpacho import get, Soup
import pandas as pd
import numpy as np
import re

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



# url = 'http://www.seasky.org/astronomy/astronomy-calendar-2021.html'
#
# html = get(url)
# soup = Soup(html)
#
# #all entries for 2021
# rows = soup.find('span')[17:]
# rows
#
# #date for first entry for 2021
# row = rows[0].text
# row
# print(type(row))
#
# #name for first entry for 20201
# date = rows[1].text
# date
# print(type(date))
#
# descriptions = soup.find('p')[6:]
# description = descriptions[0]
# description

def parser(year=2022):
    url = f'http://www.seasky.org/astronomy/astronomy-calendar-{year}.html'
    html = get(url)
    soup = Soup(html)

    rows = soup.find('span')[17:]
    descriptions = soup.find('p')[6:]

    dates = []
    full_text = []

    i = 0
    for row in rows:
        date = rows[i].text
        dates.append(date)
        i+=1
    j = 0
    for description in descriptions:
        text = descriptions[j]
        full_text.append(text)
        j+=1
    return dates, full_text

def get_dates(list_of_data):
    dates = full_list[0][0::2]
    dates = dates[:-1]
    #len(dates)
    return dates

def get_names(list_of_data):
    names = full_list[0][1::2]
    names = names[:-1]
    return names

def remove_period(list_of_names):
    name_list=[]
    for name in list_of_names:
        name = name[:-1]
        name_list.append(name)
    return name_list

def get_descriptions(list_of_data):
    descriptions = full_list[1]
    descriptions = descriptions[:-11]
    return descriptions

def get_messy_descriptions(list_of_data, year):
    i = 1
    if year == '2020':
        i = 1
    elif year == '2021':
        i = 3
    elif year == '2022':
        i = 5
    elif year == '2023':
        i = 7
    else:
        print('pick a year between 2020 and 2023')
    print(i)
    descriptions = list_of_data[i]
    descriptions = descriptions[:-11]
    return descriptions

#to extend for multiple years

events_2020_to_2023 = []

for year in [2020, 2021, 2022, 2023]:
    events_2020_to_2023.extend(parser(year=year))

def get_dates(list_of_data, year):
    i = 0
    if year == '2020':
        i = 0
    elif year == '2021':
        i = 2
    elif year == '2022':
        i = 4
    elif year == '2023':
        i = 6
    else:
        print('pick a year between 2020 and 2023')

    dates = list_of_data[i][0::2]
    dates = dates[:-1]
    return dates

dates_2020 = get_dates(events_2020_to_2023, '2020')
len(dates_2020)
dates_2021 = get_dates(events_2020_to_2023, '2021')
len(dates_2021)
dates_2022 = get_dates(events_2020_to_2023, '2022')
len(dates_2022)
dates_2023 = get_dates(events_2020_to_2023, '2023')
len(dates_2023)

def get_names(list_of_data, year):
    i = 0
    if year == '2020':
        i = 0
    elif year == '2021':
        i = 2
    elif year == '2022':
        i = 4
    elif year == '2023':
        i = 6
    else:
        print('pick a year between 2020 and 2023')

    names = list_of_data[i][1::2]
    names = names[:-1]
    return names

names_2020 = get_names(events_2020_to_2023, '2020')
names_2020 = remove_period(names_2020)
len(names_2020)


names_2021 = get_names(events_2020_to_2023, '2021')
names_2021 = remove_period(names_2021)
len(names_2021)
names_2022 = get_names(events_2020_to_2023, '2022')
names_2022 = remove_period(names_2022)
len(names_2022)
names_2023 = get_names(events_2020_to_2023, '2023')
names_2023 = remove_period(names_2023)
len(names_2023)


messy_descriptions_2020 = get_messy_descriptions(events_2020_to_2023, '2020')
len(messy_descriptions_2020)
messy_descriptions_2020


messy_descriptions_2021 = get_messy_descriptions(events_2020_to_2023, '2021')
len(messy_descriptions_2021)
messy_descriptions_2022 = get_messy_descriptions(events_2020_to_2023, '2022')
len(messy_descriptions_2022)
messy_descriptions_2023 = get_messy_descriptions(events_2020_to_2023, '2023')
len(messy_descriptions_2023)


# for item in messy_descriptions_2020:
#     item = str(item)
#     print(item)

#eventually change this to -5 in last desc line rather than -6
def clean_description(messy_description):
    d_list = []
    for desc in messy_description:
        desc = str(desc)
        #print(desc)
        desc = desc[55:]
        desc = desc[desc.find('</span> '):]
        desc = desc[8:]
        desc = desc[:-6]
        d_list.append(desc)
    return d_list

desc_2020 = clean_description(messy_descriptions_2020)
len(desc_2020)

desc_2021 = clean_description(messy_descriptions_2021)
len(desc_2021)

desc_2022 = clean_description(messy_descriptions_2022)
len(desc_2022)

desc_2023 = clean_description(messy_descriptions_2023)
len(desc_2023)

df_2020 = pd.DataFrame({
    'date': dates_2020,
    'event_name' : names_2020,
    'description' : desc_2020
})

df_2020.head(35)
df_2020.iloc[13, 2] = 'The Lyrids is an average shower, usually producing about 20 meteors per hour at its peak. It is produced by dust particles left behind by comet C/1861 G1 Thatcher, which was discovered in 1861. The shower runs annually from April 16-25. It peaks this year on the night of the night of the 21st and morning of the 22nd. These meteors can sometimes produce bright dust trails that last for several seconds. The nearly new moon will ensure dark skies for what should be a good show this year. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Lyra, but can appear anywhere in the sky.'
df_2020.tail(35)
df_2020.iloc[45, 2] = 'The Orionids is an average shower producing up to 20 meteors per hour at its peak. It is produced by dust grains left behind by comet Halley, which has been known and observed since ancient times. The shower runs annually from October 2 to November 7. It peaks this year on the night of the 21st and the morning of of the 22nd. The waxing crescent moon will set before midnight leaving dark skies for what should be a good show. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Orion, but can appear anywhere in the sky.'
df_2020.tail(30)

df_2021 = pd.DataFrame({
    'date': dates_2021,
    'event_name' : names_2021,
    'description' : desc_2021
})

df_2021.head(30)

df_2021.iloc[12, 2] = 'The Lyrids is an average shower, usually producing about 20 meteors per hour at its peak. It is produced by dust particles left behind by comet C/1861 G1 Thatcher, which was discovered in 1861. The shower runs annually from April 16-25. It peaks this year on the night of the night of the 22nd and morning of the 23rd. These meteors can sometimes produce bright dust trails that last for several seconds. The nearly full moon will be a problem this year. Its glare will block out all but the brightest meteors. But if you are patient you may still be able to catch a few good ones. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Lyra, but can appear anywhere in the sky.'
df_2021.iloc[40, 2] = 'The Orionids is an average shower producing up to 20 meteors per hour at its peak. It is produced by dust grains left behind by comet Halley, which has been known and observed since ancient times. The shower runs annually from October 2 to November 7. It peaks this year on the night of the 21st and the morning of of the 22nd. The waxing crescent moon will set before midnight leaving dark skies for what should be a good show. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Orion, but can appear anywhere in the sky.'
df_2021.tail(30)

df_2022 = pd.DataFrame({
    'date': dates_2022,
    'event_name' : names_2022,
    'description' : desc_2022
})

df_2022.head(30)
df_2022.iloc[12, 2] = 'The Lyrids is an average shower, usually producing about 20 meteors per hour at its peak. It is produced by dust particles left behind by comet C/1861 G1 Thatcher, which was discovered in 1861. The shower runs annually from April 16-25. It peaks this year on the night of the night of the 22nd and morning of the 23rd. These meteors can sometimes produce bright dust trails that last for several seconds. The nearly full moon will be a problem this year. Its glare will block out all but the brightest meteors. But if you are patient you may still be able to catch a few good ones. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Lyra, but can appear anywhere in the sky.'
df_2022.iloc[40, 2] = 'The Orionids is an average shower producing up to 20 meteors per hour at its peak. It is produced by dust grains left behind by comet Halley, which has been known and observed since ancient times. The shower runs annually from October 2 to November 7. It peaks this year on the night of the 21st and the morning of of the 22nd. The waxing crescent moon will set before midnight leaving dark skies for what should be a good show. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Orion, but can appear anywhere in the sky.'

df_2022.tail(30)

df_2023 = pd.DataFrame({
    'date': dates_2023,
    'event_name' : names_2023,
    'description' : desc_2023
})

df_2023.head(30)

df_2023.iloc[13, 2] = 'The Lyrids is an average shower, usually producing about 20 meteors per hour at its peak. It is produced by dust particles left behind by comet C/1861 G1 Thatcher, which was discovered in 1861. The shower runs annually from April 16-25. It peaks this year on the night of the night of the 22nd and morning of the 23rd. These meteors can sometimes produce bright dust trails that last for several seconds. The nearly full moon will be a problem this year. Its glare will block out all but the brightest meteors. But if you are patient you may still be able to catch a few good ones. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Lyra, but can appear anywhere in the sky.'
df_2023.iloc[40, 2] = 'The Orionids is an average shower producing up to 20 meteors per hour at its peak. It is produced by dust grains left behind by comet Halley, which has been known and observed since ancient times. The shower runs annually from October 2 to November 7. It peaks this year on the night of the 21st and the morning of of the 22nd. The waxing crescent moon will set before midnight leaving dark skies for what should be a good show. Best viewing will be from a dark location after midnight. Meteors will radiate from the constellation Orion, but can appear anywhere in the sky.'

df_2023.tail(30)

frames = [df_2020, df_2021, df_2022, df_2023]
df = pd.concat(frames)

df.info()
df.head()

df['start_year'] = '2020'

df.iloc[0:61, 3] = '2020'
df.iloc[62:116, 3] = '2021'
df.iloc[117:172, 3] = '2022'
df.iloc[173:, 3] = '2023'

#verifying years
df.iloc[172]

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
        date_end = day_list[1] + 1
    elif len_list == 1:
        date_end = day_list[0]
    return date_end

#dates cleanup
df['start_month'] = df['date'].apply(lambda x: month_generator(x))
df['day_list'] = df['date'].apply(lambda x: find_days(x))
df['start_day'] = df['day_list'].apply(lambda x: start_date(x))
df['start_day'] = df['start_day'].astype(str)

df['end_year'] = df['start_year']
df['end_month'] = df['date'].apply(lambda x: month_generator(x))
df['end_day'] = df['day_list'].apply(lambda x: end_date(x))
df['end_day'] = df['end_day'].astype(str)

df['start_date']= df['start_year'] + '-' + df['start_month'] + '-' + df['start_day']
df['end_date'] = df['end_year'] + '-' + df['end_month'] + '-' + df['end_day']

df.info()
df.head()
df = df.drop(['start_year', 'start_month', 'day_list', 'start_day', 'end_year', 'end_month', 'end_day'], axis=1)
df.head(30)


len_df = len(df)
print(len_df)
i = 0

while i < len_df:

    # If modifying these scopes, delete the file token.pickle.
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

        #create a new calendar
        # calendar = {
        # 'summary': 'Test Calendar',
        # 'timeZone': 'America/New_York'
        # }
        #
        # created_calendar = service.calendars().insert(body=calendar).execute()
        #
        # print(created_calendar['id'])
        event_name = df.iloc[i, 1]
        description = df.iloc[i, 2]
        start_date = df.iloc[i, -2]
        end_date = df.iloc[i, -1]

        #insert an event
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
            # 'attendees' : [
            #     {'email': 'melissa.c.griffin@gmail.com'}
            # ],

        }

        response = service.events().insert(
            calendarId = 'guf9674q92tdp5bboenn11btv8@group.calendar.google.com',
            body = event_request_body
        ).execute()

    if __name__ == '__main__':
        main()
    i+=1
