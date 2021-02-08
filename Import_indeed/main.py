from flask import Flask,render_template,request,redirect
from scrapper import get_jobs

app = Flask('SuperScrapper')

db = {}

@app.route('/')
def home():
    return render_template('potato.html')

@app.route('/report')
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect('/')
    return render_template('report.html',resultsNumber = len(jobs),numsearchingBy=word,jobs = jobs)

if __name__ == '__main__':
    app.run(debug=True)