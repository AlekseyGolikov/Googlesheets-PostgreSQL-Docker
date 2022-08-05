
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    def __init__(self, creds, ssid):
        """Establishing connect to Google sheets instance"""
        # Файл, полученный в Google Developer Console
        CREDENTIALS_FILE = creds # 'creds.json'
        # ID Google Sheets документа (можно взять из его URL)
        self.__spreadsheet_id = ssid # '1r4JlWmezNj_z1tbfQpf7MHSzU32Ju75zA_hsOcfrDlQ'

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.__service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def __enter__(self):
        return self

    def getData(self):
        """Read data"""
        values = self.__service.spreadsheets().values().get(
            spreadsheetId=self.__spreadsheet_id,
            range='A2:D100',
            majorDimension='ROWS'
        ).execute()
        return values

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            exit(0)
        else:
            exit(1)


if __name__=='__main__':
    with GoogleSheets('creds.json', '1r4JlWmezNj_z1tbfQpf7MHSzU32Ju75zA_hsOcfrDlQ') as sheet:
        value = sheet.getData()


# Пример записи в файл
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {"range": "A7:D7",
#              "majorDimension": "ROWS",
#              "values": [['1', '2', '3', '31.07.2022']]},
# 	]
#     }
# ).execute()
