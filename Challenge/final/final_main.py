from flask import Flask,render_template,request,redirect,send_file
from scrapper_final import get_jobs,save_to_file

app = Flask('Final_scrap')

db = {}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def report():
    term = request.args.get('term')
    if term:
        term = term.lower()
        existingJobs = db.get(term)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(term)
        db[term] = jobs
    else:
        return redirect('/')
    result = get_jobs(term)

    return render_template('list.html',result= result,term = term,len = len(result))

@app.route('/export')
def export():
    print(1)
    try:
        term = request.args.get('term')
        print(term)
        if not term:
            raise Exception()
        term = term.lower()
        result = db.get(term)
        save_to_file(result)
    except:
        return redirect('/')
    return send_file('job.csv')


if __name__ == '__main__':
    app.run(debug=True)

