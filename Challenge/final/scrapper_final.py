import requests
from bs4 import BeautifulSoup
import csv

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-python-jobs

Good luck!
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def get_url(word):
    url_list = [f'https://stackoverflow.com/jobs?r=true&q={word}',
   f'https://weworkremotely.com/remote-jobs/search?term={word}',
    f'https://remoteok.io/remote-{word}-jobs']
    return url_list

def from_stack(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    job_list = soup.find_all('div',class_='js-result')
    stack_list = []
    for item in job_list:
        title = item.find('a',class_='s-link')['title']
        company = item.find('h3',class_='fc-black-700').find('span').string
        link = 'https://stackoverflow.com'+item.find('a',class_='s-link')['href']
        stack_dic= {'title':title,'company':company,'link':link}
        stack_list.append(stack_dic)
    return stack_list

def from_wework(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text,'html.parser')
    job_ul = soup.find('section',class_='jobs').find('ul')
    job_ol = job_ul.find_all('li')
    wework_list = []
    for item in job_ol[:-1]:
        title = item.find('span',class_='title').string
        company = item.find('span',class_='company').string
        link = 'https://weworkremotely.com/'+item.find('a')['href']
        wework_dic = {'title': title, 'company': company, 'link': link}
        wework_list.append(wework_dic)
    return wework_list

def from_remoteok(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text,'html.parser')
    jobsboard = soup.find('table',id='jobsboard')

    tr_list = jobsboard.find_all('tr',class_='remoteok-original')

    result = []
    for item in tr_list:
        link = 'https://remoteok.io/'+item['data-url']
        td = item.find('td',class_='company_and_position_mobile')
        td_list = td.find_all('a',class_='preventLink')
        item_dic = {}
        company,title = 0,0
        for i in td_list:
            if i.find('h2'):
                title = i.find('h2').string
            elif i.find('h3'):
                company = i.find('h3').string

            if company != 0 and title!=0:
                item_dic ={'title':title,'company':company,'link' : link}
                result.append(item_dic)
                company,title = 0,0
    return result


def save_to_file(jobs):
    file = open("job.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title,company,link"])
    for value in jobs:
        writer.writerow(value.values())
    return

def get_jobs(word):
    url_list = get_url(word)
    result = []
    result += from_stack(url_list[0])
    result += from_wework(url_list[1])
    result += from_remoteok(url_list[2])
    return result