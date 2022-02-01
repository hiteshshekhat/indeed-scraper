import requests
# import requests_cache
from bs4 import BeautifulSoup
from time import time
import json
import random



# requests_cache.install_cache(expire_after=18000, allowable_methods=('GET', 'POST'))





base_url = 'https://es.indeed.com'


with open("proxies_ip.txt", "r") as f:
    proxies=f.read().splitlines()


def send_request(url, proxies):
    while True:
        proxy = proxies[random.randint(0, len(proxies)-1)]
        try:
            # proxies = {"http": 'http://' + proxies(proxy), "https": 'https://' + proxies(proxy)}
            response = requests.get(url, timeout=5, proxies={"http": 'http://' + proxy, "https": 'https://' + proxy})
            print(response.status_code)
            print("Proxy currently being used")
            break
        except:
            print("Error, looking for another proxy")
    return response


''' Get list for Alphabatical urls '''

url = base_url + '/browsejobs'
r = requests.get(url)
r = r.text
html_soup = BeautifulSoup(r, 'html.parser')
nav_alphabates = html_soup.find('ul', {'id':'title'})
list_nav_urls = [base_url + a['href'] for a in nav_alphabates.select('li>a')]
print(list_nav_urls)
print(len(list_nav_urls))



for url in list_nav_urls:
    print(url)
    job_dict = {'letter':url[-1], 'seen_on_url':url, 'seen_epoch':time()}
    r = send_request(url, proxies)
    r = r.text
    html_soup = BeautifulSoup(r, 'html.parser')
    jobs_ul = html_soup.find('ul', {'class':'letter_companies'})
    try:
        jobs_li = jobs_ul.select('li', {'class':'letter_company_name'})
        for li_tag in jobs_li:
            print(jobs_li.index(li_tag))
            print('#############################')
            a = li_tag.find('p').find('a')
            job_title = a.text
            job_serach_url = base_url + a['href']
            job_dict['job_title'] = job_title
            job_dict['job_search_url'] = job_serach_url
            print(job_dict)
            with open('es_jobs_detail.jsonl', 'a') as f:
                json.dump(job_dict, f)
                f.write('\n')
    except AttributeError:
        print(f"Page doesn't work for letter {url[-1]}")
        



