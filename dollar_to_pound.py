from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=GBP')
soup = BeautifulSoup(source.text, 'lxml')
conversion = float(soup.find(class_='result__BigRate-sc-1bsijpp-1 iGrAod').text.split()[0])
