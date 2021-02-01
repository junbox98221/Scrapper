import requests
import csv
from bs4 import BeautifulSoup

main_url = "http://www.alba.co.kr/"

def get_company_list(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    brand_list = soup.find('div',{'id':'MainSuperBrand'})
    ul_list = brand_list.find('ul',class_='goodsBox')
    a_list = ul_list.find_all('a',class_='goodsBox-info')
    url_list = []
    for i in a_list:
        url_list.append(i.attrs['href'])
    return url_list

def get_alba_list(company_url):
    final_list = []
    for url in company_url:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        NormalInfo_list = soup.find('div',{'id':'NormalInfo'})
        tbody = NormalInfo_list.find('tbody')
        tr_list = tbody.find_all('tr')
        for tr in tr_list:
            if tr.find('td',class_='local first'):
                city = tr.find('td',class_='local first').get_text()
            if tr.find('td',class_='title'):
                place = tr.find('td',class_='title').find('span',class_='company').string
            if tr.find('td',class_='data'):
                time = tr.find('td',class_='data').string
            if tr.find('td',class_='pay'):
                pay = tr.find('td',class_='pay').get_text()
            if tr.find('td',class_='regDate last'):
                minute = tr.find('td',class_='regDate last').string
            final_list.append([city,place,time,pay,minute])

    return final_list

def save_to_file(jobs):
    file = open("day7job.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["place,title,time,pay,date"])
    for job in jobs:
        writer.writerow(job)
    return


url_list = get_company_list(main_url)
jobs = get_alba_list(url_list)
save_to_file(jobs)