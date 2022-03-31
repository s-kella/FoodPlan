import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def add_to_gsheet(first_name, last_name=''):
    gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    gcredentials = os.getenv('GOOGLE_SHEETS_KEY')
    gdocument = 'foodPlan'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1
    wks.append_row([first_name, last_name])
    