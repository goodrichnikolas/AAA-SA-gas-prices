from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import decimal
import time
import random
import tqdm
import json
import glob
import os

url = 'https://gasprices.aaa.com/?state='
todays_date = time.strftime("%m-%d-%Y")

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
            'DC', 'PR', 'VI']

def priceScraper(url, state):
    df_rows = []
    url += state
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    cities = soup.find_all('h3')

    for cityRow in cities:
        city_name = cityRow.text
        # print('------------------------------------------------------')
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

            city_dict[label] = {
                'Regular': regularGasPrice,
                'Diesel': dieselGasPrice,
                'Mid': midGasPrice,
                'Premium': premiumGasPrice
            }
            
            dict_to_df = {
                'State': state,
                'City': city_name,
                'Label': label,
                'Regular': regularGasPrice,
                'Diesel': dieselGasPrice,
                'Mid': midGasPrice,
                'Premium': premiumGasPrice
            }
            df_rows.append(dict_to_df)
            
    df = pd.DataFrame(df_rows)
    df.to_csv(f'./AAA Gas/AAA-SA-gas-prices/states_csvs/gas_prices_{state}.csv', index=False)
        

    

def combine_csvs():
    #print cwd
    print(os.getcwd())
    all_files = glob.glob('./states_csvs/*.csv')
    df = pd.concat([pd.read_csv(f) for f in all_files])
    df.to_csv(f'./AAA Gas/AAA-SA-gas-prices/combined_csvs/gas_prices_combined_{todays_date}.csv', index=False)
    
    
def get_gas_prices(states):
    for state in tqdm.tqdm(states):
        print(f'Getting data for {state}')
        state_dict = priceScraper(url, state)
        #random sleep to avoid getting blocked
        time.sleep(random.randint(1, 5))
        
        
def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
def main():
    #get_gas_prices(states)
    #Combine all csv files into one
    #Creat combined csv folder if not exists
    create_folder_if_not_exists('./combined_csvs')
    combine_csvs()
        
    
if __name__ == "__main__":
    main()