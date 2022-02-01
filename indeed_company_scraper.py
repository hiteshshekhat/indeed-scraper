from ctypes import c_ushort
import requests
# import requests_cache
from bs4 import BeautifulSoup
from time import time
import json
import random


# requests_cache.install_cache(expire_after=18000, allowable_methods=('GET', 'POST'))


# Reading company urls
with open('random_5000_urls.jsonl','r') as f:
    lines = f.readlines()

company_url_dict = [json.loads(url) for url in lines]


# Reading proxies
with open("proxies_ip.txt", "r") as f:
    proxies=f.read().splitlines()


# function to make request with rotating proxy
def send_request(url, proxies):
    while True:
        proxy = proxies[random.randint(0, len(proxies)-1)]
        try:
            # proxies = {"http": 'http://' + proxies(proxy), "https": 'https://' + proxies(proxy)}
            response = requests.get(url, proxies={"http": 'http://' + proxy, "https": 'https://' + proxy})
            print("Proxy currently being used")
            break
        except:
            print("Error, looking for another proxy")
    return response



for item in company_url_dict[2397:2401]:
    url = item['company_url']
    # proxy = proxies[random.randint(0, len(proxies)-1)]
    # r = requests.get(url, proxies={"http": 'http://' + proxy, "https": 'https://' + proxy})
    r = send_request(url, proxies)
    r = r.text
    html_soup = BeautifulSoup(r, 'html.parser')
    ul_= html_soup.find('ul', attrs={'class':'css-4bze3a eu4oa1w0'})
    try:
        a_tags = ul_.select('li>a')
        company_details = {'company_url':url}
        for a in a_tags:
            title = a.find('span').text
            if title == 'Reviews':
                if len(a.text) > 7:
                    try:
                        company_details['reviews_count'] = int(a.text[:-7])
                    except ValueError:
                        company_details['reviews_count'] = int(float(a.text[:-8])*1000)
                else:
                    company_details['reviews_count'] = 0
                # print(a.text[:-7])
            elif title == 'Salaries':
                if len(a.text) > 8:
                    try:
                        company_details['salaries_count'] = int(a.text[:-8])
                    except ValueError:
                        company_details['salaries_count'] = int(float(a.text[:-9])*1000)
                else:
                    company_details['salaries_count'] = 0
            elif title == 'Jobs':
                if len(a.text) > 4:
                    try:
                        company_details['jobs_count'] = int(a.text[:-4])
                    except ValueError:
                        company_details['jobs_count'] = int(float(a.text[:-5])*1000)
                else:
                    company_details['jobs_count'] = 0
                company_details['seen_epoch'] = time()


        with open('company_details1.jsonl', 'a') as outfile:
                json.dump(company_details, outfile)
                outfile.write('\n')
    except AttributeError:
        print(f'{url} not working.....')


