import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# получить страницы и записать их в переменную, страницы берем из файла
file = open('site.txt', 'r')
page = file.read().split('\n')
file.close()

# проверка статус кода страниц и запись в переменную
status_cod = []
for item in page:
    s = requests.get(item, allow_redirects=False).status_code
    status_cod.append(s)

#доступ к google docs
scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('TestPython-c628e5e535bd.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('Test').sheet1

#добавление строки в таблицу в докс
for i in range(len(page)):
    wks.append_row([page[i], status_cod[i]])

print('Congratulations!')