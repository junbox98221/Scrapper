import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python&sort=i"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page=pages[-2].get_Text(strip=True)
    return int(last_page)

def extract_job(html):
    title = html.find('h2').find('a')['title']
    company,location = html.find('h3').find_all(
        'span',recursive = False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip('-').strip(' \r').strip('\n')
    job_id = html['data-jobid']
    return{
        'title':title,
        'company':company,
        'location':location,
        'apply_link':f'https://stackoverflow.com/jobs/{job_id}'
    }