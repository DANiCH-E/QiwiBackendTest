import requests
import datetime
from bs4 import BeautifulSoup
import click

@click.command()
@click.option('--code', default='USD', help='Enter the currency in ISO 4217 format')
@click.option('--date', default='2022-10-08', help='Enter the date in YYYY-MM-DD format')

def getData(code, date):
    if parse_data(date) == False:
        return False

    html_file = ("test.html")
    html_file = open(html_file, encoding='UTF-8').read()
    soup = BeautifulSoup(html_file, 'xml')
    fl = False

    for char_code in soup.find_all('CharCode'):
        if code in char_code:
            fl = True
            click.echo(f'{char_code.contents[0]} ({char_code.find_next("Name").contents[0]}): {char_code.find_next("Value").contents[0]}')
            
    # Проверка на корректность ввода валюты
    if fl == False:
        print("Incorrect currency value. Try again")


def parse_data(date):
    # Преобразование даты в нужный формат и проверка на корректность ввода даты
    try:
        format_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
        url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={format_date}'
    except ValueError:
        click.echo('Incorrect data format. Try again')
        return False

    # Получение данных и запись в файл
    r = requests.get(url)
    soup_ing = str(BeautifulSoup(r.content, 'xml'))
    soup_ing = soup_ing.encode()
    with open("test.html", "wb") as file:
        file.write(soup_ing)

if __name__ == '__main__':
    getData()

