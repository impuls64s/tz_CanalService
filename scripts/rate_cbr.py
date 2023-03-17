import requests
from datetime import datetime
import xml.etree.ElementTree as ET


# Функция проверяет актуальность даты в файле cbr.xml,
# если дата не актуально делаем запрос на сервер и обновляем файл.
# В качестве аргумента принимает суммув USD, возвращает сумму в рублях
def usd_exchange_rate(price_usd):
    today = datetime.now().strftime("%d/%m/%Y")

    tree = ET.parse('scripts/cbr.xml')
    root = tree.getroot()
    date_xml = root.attrib.get('Date').replace('.', '/')

    if date_xml != today:
        resp = requests.get(
            f'https://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={today}'
        )
        with open('scripts/cbr.xml', 'w') as file:
            file.write(resp.text)
        usd_exchange_rate(price_usd)

    for country in root.findall('Valute'):
        char_code = country.find('CharCode').text
        
        if char_code == 'USD':
            value = country.find('Value').text.replace(',', '.')
            result = float(value) * price_usd
            return result
