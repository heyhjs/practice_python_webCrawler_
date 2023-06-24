from flask import Flask, redirect, render_template, request, send_file

from extractors.remote import extract_remote_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def hello():
    kw = request.args.get("keyword")
    if kw == None or kw == "":
        return redirect("/")
    if kw in db:
        jobs = db[kw]
    else:
        remote = extract_remote_jobs(kw)
        wwr = extract_wwr_jobs(kw)
        jobs = remote + wwr
        db[kw] = jobs
    return render_template("search.html", keyword=kw, jobs=jobs)


@app.route("/export")
def export():
    kw = request.args.get("keyword")
    if kw == None:
        return redirect("/")
    if kw not in db:
        return redirect(f"/search?keyword={kw}")
    save_to_file(kw, db[kw])
    return send_file(f'{kw}.csv', as_attachment=True)


app.run("0.0.0.0")
