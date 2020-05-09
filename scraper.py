# ALL THE MODULES ARE HERE
import requests
import requests_cache
from bs4 import BeautifulSoup
from datetime import timedelta
from time import sleep
from peewee import DoesNotExist
from urllib.parse import parse_qs, urlparse


requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET')
)

url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'
# query_str = urlparse(url).query 
# id = parse_qs(query_str)['ID'][0].strip(),

#FUNCTIONS BELOW

def get_detainee_details():

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    all_detainees = soup.find('div', id_='content')
    detainee_data = all_detainees.find_all('td')

    return detainee_data


#MAIN FUNCTION BELOW
def main():
    print('Printing main function...')
    print(get_detainee_details())

if __name__=='__main__':
    main()
