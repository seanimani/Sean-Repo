from bs4 import BeautifulSoup
import requests
import re
from dollar_to_pound import conversion
import sys

print('Website: https://newegg.com')
search_term = input('What product would you like to search for?\n>')
url = f'https://www.newegg.com/p/pl?d={search_term}&quicklink=true&N=4131'
source = requests.get(url)
soup = BeautifulSoup(source.text, 'lxml')

try:
    pages = soup.find(class_='list-tool-pagination').strong.text
    number_of_pages = int(pages.split('/')[1])
except AttributeError:
    print('https://newegg.com does not have that item')
    sys.exit(1)

# print(number_of_pages)

items_found = {}

for page in range(1, number_of_pages + 1):
    url = f'https://www.newegg.com/p/pl?d={search_term}' \
          f'&quicklink=true&N=4131&page={page}'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    div = soup.find(class_='item-cells-wrap border-cells'
                           ' items-grid-view four-cells expulsion-one-cell')
    items = div.find_all(text=re.compile(search_term, re.IGNORECASE))
    for item in items:
        parent = item.parent
        if parent.name != 'a':
            continue

        link = parent['href']
        # print(link)

        # next_parent = parent.parent.parent
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_='price-current').strong.string
            # print(price)
            items_found[item] = {'price': int(
                price.replace(',', '')) * conversion, 'link': link}
        except AttributeError:
            pass

sorted_items = list(
    reversed(sorted(items_found.items(), key=lambda x: x[1]['price'])))

for item in sorted_items[:-1]:
    print(f"Name: {item[0]}")
    print(f"Price: £{item[1]['price']}")
    print(f"link: {item[1]['link']}")
    print('--------------------------------')

print('\n\n\n\n')
print(f'Cheapest {search_term} is...')
print(f"Name: {sorted_items[-1][0]}")
print(f"Price: £{sorted_items[-1][1]['price']}")
print(f"link: {sorted_items[-1][1]['link']}")
