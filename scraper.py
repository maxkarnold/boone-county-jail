# ALL THE MODULES ARE HERE
import requests
import requests_cache
from bs4 import BeautifulSoup
from datetime import timedelta
from time import sleep
from peewee import DoesNotExist
from urllib.parse import parse_qs, urlparse
from models import Detainee_Info, Detainee_Charges

requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET')
)

url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'
# query_str = urlparse(url).query 
# id = parse_qs(query_str)['ID'][0].strip(),

# url = soup.select("div#content > div",recursive=False)
#
# for tag in url:
#     div_ID = tag.get('id')
#     ids = div_ID.lstrip('mugshot')
#     print(ids)

#FUNCTIONS BELOW

def get_main_url():
    r = requests.get(url, headers ={
    'user-agent': "I'm good people!!!"})

    r.raise_for_status()
    return r.content

def extract_detainee_containers(main_url):
    soup = BeautifulSoup(main_url, 'lxml')

    detainee_names = set()

    detainee_tables = soup.find_all('div',class_='mugshotDiv')

    for detainee in detainee_tables:
        detainee_name_cell = detainee.find('div',class_='inmateName')
        detainee_name = detainee_name_cell.text.strip()
        detainee_names.add(detainee_name)
    return detainee_names

def get_detainee_container(detainee_name, detainee_names):
    soup = BeautifulSoup('main_url', 'lxml')


    # detainee_tables = soup.find_all('div',class_='mugshotDiv')
    # detainee_name_cell = detainee.find('div', class_='inmateName')
    # detaineee_name = detainee_name_cell.text.strip()

    for detainee_name in detainee_names:
        print(detainee_name)
        print(type(detainee_name))
        print(type(detainee_names))
        detainee_name_cell = soup.find(detainee_name)
        print(detainee_name_cell)
        detainee = detainee_name_cell.find_parent('div', class_='mugshotDiv')
    return detainee

def extract_detainee_details(detainee_tables,detainee_names):

    detainee_name_cell = detainee.find('div',class_='inmateName')
    detainee_info_tables = detainee.find('div', class_='infoContainer')
    detainee_info_cells = detainee_info_tables.find_all(
        'td',class_='two td_left'
    )

    Detainee_Info.create(
        name= detainee_name_cell.text.strip(),
        height=detainee_info_cells[0].text.strip(),
        weight=detainee_info_cells[1].text.strip(),
        sex=detainee_info_cells[2].text.strip(),
        eyes=detainee_info_cells[3].text.strip(),
        hair=detainee_info_cells[4].text.strip(),
        race=detainee_info_cells[5].text.strip(),
        age=detainee_info_cells[6].text.strip(),
        city=detainee_info_cells[7].text.strip(),
        state=detainee_info_cells[8].text.strip(),
    )

def extract_detainee_charges(detainee_tables, detainee_names):

    detainee_name_cell = detainee.find('div',class_='inmateName')
    detainee_info_tables = detainee.find('div', class_='chargesContainer')
    detainee_charge_row = detainee_info_tables.find('tr')
    detainee_charge_cells = detainee_charge_row.find_all(
        'td',class_='two td_left'
    )

    Detainee_Charges.create(
        name=detainee_name_cell.text.strip(),
        case_num=detainee_charge_cells[0].text.strip(),
        charge_description=detainee_charge_cells[1].text.strip(),
        charge_status=detainee_charge_cells[2].text.strip(),
        bail_amount=detainee_charge_cells[3].text.strip(),
        bond_type=detainee_charge_cells[4].text.strip(),
        court_date=detainee_charge_cells[5].text.strip(),
        court_time=detainee_charge_cells[6].text.strip(),
        court_jur=detainee_charge_cells[7].text.strip(),
    )


#MAIN FUNCTION BELOW
def main():
    print('executing scraper')
    main_url = get_main_url()
    detainee_names = extract_detainee_containers(main_url)

    for detainee_name in detainee_names:
        print('checking for %s' % detainee_name)
        try:
            Detainee_Info.get(name=detainee_name)
        except DoesNotExist:
            print('extracting detainee info for %s' % detainee_name)
            detainee = get_detainee_container(detainee_name, detainee_names)
            extract_detainee_details(detainee)
            print('done')
            sleep(0.5)
        else:
             print('%s or %s already exists' % detainee_name, case_num)
    #     print('checking for %s' % case_num)
    #     try:
    #         Detainee_Charges.get(case_num=case_num)
    #     except DoesNotExist:
    #         print('extracting detainee charges for %s' % detainee_name)
    #         extract_detainee_charges(case_num)
    #         print('done')
    #         sleep(0.5)
    #     else:
    #         print('%s or %s already exists' % detainee_name, case_num)
    #
    #     sleep(1.5)

if __name__=='__main__':
    main()

#NOTES

#Haven't taken into account there could be multiple detainees with the same case number
#There could be problems with how the tables are named
#Could be problems with....
