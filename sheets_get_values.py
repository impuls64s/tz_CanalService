from __future__ import print_function
from datetime import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1YQ8aSsxAe36w25PmsAgAkk21Ij6hXafh3OAYQ8xpCzw'
SAMPLE_RANGE_NAME = 'List!A2:D'


def get_values():

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        
        try:
            result = []
            for item in values:
                result.append(
                    (
                        int(item[0]),
                        int(item[1]),
                        int(item[2]),
                        datetime.strptime(item[3], "%d.%m.%Y").date()
                    )
                )
        except IndexError:
            print('[-] Не все поля таблицы заполнены. Ожидание 5 сек')
            time.sleep(5)
            get_values()

    except HttpError as err:
        print(err)
    
    return result


def main():
    get_values()


if __name__ == '__main__':
    main()
