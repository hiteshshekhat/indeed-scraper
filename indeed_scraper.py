from cgitb import html
import requests
import requests_cache
from bs4 import BeautifulSoup


requests_cache.install_cache(expire_after=18000, allowable_methods=('GET', 'POST'))


base_url = 'https://www.indeed.com'


''' Get list for Alphabatical urls '''

url = base_url + '/companies/browse-companies/'
r = requests.get(url)
r = r.text
html_soup = BeautifulSoup(r, 'html.parser')
nav_alphabates = html_soup.find('ul', {'class':'css-3h4rxa-Box eu4oa1w0'})
list_nav_urls = [base_url + a['href'] for a in nav_alphabates.select('li>a')]
# print(list_nav_urls)



for url in list_nav_urls[0:1]:
    r = requests.get(url)
    r = r.text
    html_soup = BeautifulSoup(r, 'html.parser')
    pagination_ul = html_soup.find('ul', {'class':'css-14v4tts-Box eu4oa1w0'})
    pagination_urls = [base_url + a['href'] for a in pagination_ul.select('li>a')]
    # print(pagination_urls)


for url in pagination_urls[0:2]:
    r = requests.get(url)
    r = r.text
    html_soup = BeautifulSoup(r, 'html.parser')
    ul_ = html_soup.find('ul', {'class':'css-kbd3oo-Flex e37uo190'})
    # print(ul_)
    company_urls = [base_url + a['href'] for a in ul_.find_all('a', {'class':'css-pid9e1-Link emf9s7v0'})]
    print(company_urls)
    print(len(company_urls))
    with open("urls.txt", "a") as f:
        f.write("\n".join(company_urls))
        f.write('\n')