# ALL THE MODULES ARE HERE
import requests
import requests_cache
from bs4 import BeautifulSoup
from datetime import timedelta
from time import sleep
from peewee import DoesNotExist
from models import Detainee_Info, Detainee_Charges

requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET')
)

url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'


r = requests.get(url, headers ={
'user-agent': "I'm good people!!!"})

soup = BeautifulSoup(r.content, 'lxml')

#FUNCTIONS BELOW

def get_detainee_divs(soup):

    details_page = soup.find(id='content')
    mugshot_divs = details_page.find_all('div', class_='mugshotDiv')
    
    return mugshot_divs

def extract_id(div):

    mugshot_id = div.attrs['id'].lstrip('mugshot')

    return mugshot_id

def extract_name(div):
    
    name_div = div.find('div',class_='inmateName')
    name = name_div.text.strip()

    return name

def extract_case_num_tds(div):

    case_num_tds= div.find_all('td', attrs={"data-th": "Case #"})

    return case_num_tds
    
def create_info_table(div):

    mugshot_id = div.attrs['id'].lstrip('mugshot')
    name_div = div.find('div', class_='inmateName')
    name = name_div.text.strip()

    info_div = div.find('div', class_='infoContainer')
    trs = info_div.find_all('tr')
    
    data = {'height': "N/A", 'weight': "N/A", 'sex': "N/A",
            'eyes': "N/A", 'hair': "N/A", 'race': "N/A", 
            'age': "N/A", 'city': "N/A", 'state': "N/A", }

    for tr in trs:
        tds = tr.find_all('td')
        key = tds[0].text.lower().strip()
        value = tds[1].text.strip()
        data[key] = value

    Detainee_Info.create(
        detainee_id = mugshot_id,
        name = name,
        height = data['height'],
        weight = data['weight'],
        sex = data['sex'],
        eyes = data['eyes'],
        hair = data['hair'],
        race = data['race'],
        age = data['age'],
        city = data['city'],
        state = data['state'],
    )

def create_charge_table(case_num_td,div):

    mugshot_id = div.attrs['id'].lstrip('mugshot')
    name_div = div.find('div', class_='inmateName')
    name = name_div.text.strip()

    tr = case_num_td.find_parent('tr')

    data = {}

    for td in tr.find_all('td'):
        key = td.attrs['data-th'].lower().strip()
        value = td.text.strip()
        data[key] = value

    Detainee_Charges.create(
        detainee_id=mugshot_id,
        name=name,
        case_num=data['case #'],
        charge_description=data['charge description'],
        charge_status=data['charge status'],
        bail_amount=data['bail amount'],
        bond_type=data['bond type'],
        court_date=data['court date'],
        court_time=data['court time'],
        court_of_jurisdiction=data['court of jurisdiction'],
    )


#MAIN FUNCTION BELOW
def main():
    print('executing scraper')
    mugshot_divs = get_detainee_divs(soup)

    for div in mugshot_divs:
        mugshot_id = extract_id(div)
        name = extract_name(div)
        case_num_tds = extract_case_num_tds(div)

        print('checking %s info' % name)
        try:
            Detainee_Info.get(detainee_id=mugshot_id)
        except DoesNotExist:
            create_info_table(div)
            print('adding %s info' % name)
            print('done')
        else:
            print('%s already exists' % name)

        print("checking %s's charges" % name)
        for case_num_td in case_num_tds:
            case_num = case_num_td.text.lower().strip()
            try:
                create_charge_table(case_num_td, div)
                print('adding Case# %s' % case_num)
            except DoesNotExist:
                print('%s already exists' % case_num)
        print("finished with detainee %s" % name)
        sleep(1.5)
    print('FINALLY DONE SCRAPING!!!')

if __name__=='__main__':
    main()
