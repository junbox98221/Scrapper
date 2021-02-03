import requests
from flask import Flask, render_template, request
base_url = "http://hn.algolia.com/api/v1"

app = Flask("DayNine")

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

db = {}

def make_detail_url(id):
  return f"{base_url}/items/{id}"

@app.route('/')
def get_polular():
    global popular,new
    type = popular
    type_string = request.args.get('order_by')
    if type_string == 'New':
        type = new

    html = requests.get(f'{type}').json()['hits']
    item_list = []
    for item in html:
        try:
            if db[item['objectID']]:
                item_list.append(db[item['objectID']])
        except:
            step_item = {}
            step_item['title'] = item['title']
            step_item['url'] = item['url']
            step_item['points']= item['points']
            step_item['author']= item['author']
            step_item['objectID']= item['objectID']
            step_item['id_url'] = make_detail_url(item['objectID'])
            db[item['objectID']] = step_item
            item_list.append(step_item)
    return render_template('index.html', lists = item_list, type = type_string)

@app.route('/<id>')
def get_comment(id):
    item_html = requests.get(f'http://hn.algolia.com/api/v1/items/{id}').json()
    detail_html= item_html['children']
    comment = []
    for comments in detail_html:
        try:
            if comments['author']:
                step_item = {}
                step_item['id'] = comments['author']
                step_item['text'] = comments['text']
                comment.append(step_item)
        except:
            pass
    return render_template('detail.html',comment = comment,title = item_html['title'],point = item_html['points'],url = item_html['url'],author = item_html['author'],comment_list=comment)



if __name__ == '__main__':
    app.run(debug=True)


