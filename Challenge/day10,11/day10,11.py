import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

app = Flask("DayEleven")

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

@app.route('/')
def home():
    return render_template('home.html')

def url_form(subreddit):
    url = f'https://www.reddit.com/r/{subreddit}/top/?t=month'
    return url

def url_request(url,key):
    html_source = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_source.text, "html.parser")
    news_html = soup.find_all('div',class_='_1poyrkZ7g36PawDueRza-J')

    news_list_url = []
    for news in news_html:
        news_dic = {}
        title = news.find('h3',class_='_eYtD2XCVieq6emjKBH3m').string
        link = news.find('a')['href']
        upvote = news.find('div',class_='_1rZYMD_4xY3gRcSS3p8ODO').string
        news_dic['title'] = title
        news_dic['link'] = link
        news_dic['upvote'] = upvote
        news_dic['key'] = key
        news_list_url.append(news_dic)
    return news_list_url

@app.route('/read')
def read():
    args_dic = request.args
    url_list = []
    for subreddit in args_dic.keys():
        url = url_form(subreddit)
        url_list.append(url)
    news_list = []


    for url in url_list:
        for key in args_dic.keys():
            news_list.append(url_request(url,key))

    return render_template('read.html',news_list = news_list)

app.run()