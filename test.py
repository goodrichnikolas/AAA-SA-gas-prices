from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def priceScraper(url, state):
    return_dict = {
        state: {}
    }
    url += state
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    cities = soup.find_all('h3')

    for cityRow in cities:
        city_name = cityRow.text
        print('------------------------------------------------------')
        print(city_name)

        # range 1 - 5, current, yesterday, week ago, month ago, year ago
        labels = ['Current', 'Yesterday', 'Week Ago', 'Month Ago', 'Year Ago']
        city_dict = {}

        for i, label in enumerate(labels):
            priceRow = cityRow.find_next_sibling().find_all('tr')[i+1]
            regularGasPrice = float(priceRow.find_all('td')[1].text[1:])
            midGasPrice = float(priceRow.find_all('td')[2].text[1:])
            premiumGasPrice = float(priceRow.find_all('td')[3].text[1:])
            dieselGasPrice = float(priceRow.find_all('td')[4].text[1:])

            print(f'{label} Regular Gas Price: {regularGasPrice}')            
            print(f'{label} Mid Gas Price: {midGasPrice}')
            print(f'{label} Premium Gas Price: {premiumGasPrice}')
            print(f'{label} Diesel Gas Price: {dieselGasPrice}')
            city_dict[label] = {
                'Regular': regularGasPrice,
                'Diesel': dieselGasPrice,
                'Mid': midGasPrice,
                'Premium': premiumGasPrice
            }

        return_dict[state][city_name] = city_dict

    return return_dict

#Texas
priceScraper('https://gasprices.aaa.com/?state=', 'TX')