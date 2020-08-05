#app.py
from flask import Flask, request, render_template
import urllib

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.dates import date2num

from io import BytesIO

import pandas as pd
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)

#データを読み込んでおく
df = pd.read_csv('owid-covid-data.csv', index_col = 0, parse_dates=["date"])
#データを読み込んだら、国の数だけチェックボックスを作る
fig, ax = plt.subplots(1,1)

#半日おきに新しいデータをダウンロードする
def download_csv():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    title = "./owid-covid-data.csv"
    urllib.request.urlretrieve(url,"{0}".format(title))
    df = pd.read_csv('owid-covid-data.csv', index_col = 0, parse_dates=["date"])
    print("updated the DataFrame! The time is      :", time.ctime())    
    
#ページの描写
@app.route("/")
def index():
    #国名を読み込む
    countries=""
    for location, data in df.groupby('location'):
        countries+='<input type="checkbox" name="country" value="' + location + '" id="country_' + location + '">'+'<label for="country_' + location + '">'+location+'</label>'
    return render_template("index.html",countries=countries)

   
@app.route("/plot/covid", methods=['GET',"POST"])
def plot_covid():
    # Obtain query parameters
    start = datetime.strptime(request.args.get("startdate", default="2020-03-13", type=str), "%Y-%m-%d")
    end = datetime.strptime(request.args.get("enddate", default="2020-05-05", type=str), "%Y-%m-%d")
    countries=request.args.get("country", default="Japan", type=str)
    countries=countries.split(".")
    column=request.args.get("column", default="total_cases", type=str)
    column+=request.args.get("per_milion", default="", type=str)
    
    if start > end:
        start, end = end, start
    if (start + timedelta(days=7)) > end:
        end = start + timedelta(days=7)

    png_out = BytesIO()

    #グラフの描写
    itr=0
    new_df=df[df['location'].isin(countries)]
    plt.cla()
    for location, data in new_df.groupby('location'):
        ax.plot(data["date"],data[column],label=location,marker='o',ms=1)
        itr+=1
    ax.legend( loc='upper left', borderaxespad=0)
    
    ax.set_xlim([start, end])
    ax.set_ylabel(column)
    plt.xticks(rotation=30)
   
    #Bytesioを用いた転送
    plt.savefig(png_out, format="png", bbox_inches="tight")
    img_data = urllib.parse.quote(png_out.getvalue())

    return "data:image/png:base64," + img_data

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(download_csv,'interval',hours=6)
    sched.start()
    try:
        app.run(port=5000)
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()
