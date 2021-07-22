from flask import Flask, request, render_template
from Helpers.datahelper import ReadPdfFile, MakePPT
from Helpers.docx import Word
from Helpers.email import Gmail
import time
from Helpers.Books import bible_config
import datetime

import os
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def home():
    return render_template("init.html")

@app.route('/init', methods=["POST"])
def init():
    account = request.values['account']
    password = request.values['password']
    if account == 'church_ppt' and password == 'churchchurch':
        return 'good'
    else:
        return 'error'

@app.route('/makePPT')
def makePPT():
    return render_template("index.html")



@app.route('/bible_info', methods=["POST"])
def bible_info():
    bible = bible_config.passage_data
    return bible

@app.route('/getPdfFile', methods=["POST"])
def getPdfFile():
    sermonTitle = request.values['sermon_title']
    closingSongName = request.values['closing_song']
    sr_info = request.form.get('sr_info')
    sr_version = request.form.get('sr_version')
    sis_info = request.form.get('sis_info')
    sis_version = request.form.get('sis_version')
    annocement = request.form.get('annocement')
    receivers = request.form.get('receivers')


    sr_info = json.loads(sr_info)["sr_info"]
    sr_version = json.loads(sr_version)["sr_version"]
    sis_info = json.loads(sis_info)["sis_info"]
    sis_version = json.loads(sis_version)["sis_version"]
    annocement = json.loads(annocement)["annocement"]
    receivers = json.loads(receivers)["receivers"]


    readPdfFile = ReadPdfFile()
    chineseScrpitureReading = readPdfFile.getChieseScripture(sr_info)
    chineseScrpitureInSermon = readPdfFile.getChieseScripture(sis_info)
    englishScrpitureReading = {"verses" : sr_info , "bibleVersion" : sr_version}
    englishScrpitureInSermon = {"verses" : sis_info , "bibleVersion" : sis_version}

    closingSong = readPdfFile.getClosingSong(closingSongName)
    blessing_song = readPdfFile.getBlessingSong()

    d = datetime.date.today()
    while d.weekday() != 6:
        d += datetime.timedelta(1)
    date = d


    data = {"annocement": annocement, "englishScrpitureReading": englishScrpitureReading,
            "chineseScrpitureReading": chineseScrpitureReading, "englishScrpitureInSermon": englishScrpitureInSermon,
            "chineseScrpitureInSermon": chineseScrpitureInSermon, "sermonTitle": sermonTitle, "date": date,
            "closingSongName": closingSongName, "closingSong": closingSong, "blessing_song": blessing_song}

    print('englishScrpitureReading : ',englishScrpitureReading["verses"])
    print('chineseScrpitureReading : ',chineseScrpitureReading)
    print('englishScrpitureInSermon : ',englishScrpitureInSermon["verses"])
    print('chineseScrpitureInSermon : ',chineseScrpitureInSermon)

    if len(englishScrpitureReading["verses"]) != len(chineseScrpitureReading):
        return 'Error'
    elif len(englishScrpitureInSermon["verses"]) != len(chineseScrpitureInSermon):
        return 'Error'

    else:
        start = time.time()
        threads = []
        threads.append(MakePPT(data))   # make ppt
        threads[0].start()
        threads.append(Word(data))      # make word
        threads[-1].start()

        for t in threads:
            t.join()
        end = time.time()
        print(f'total cost for ppt and docx : {end - start} sec')

        # Send Email
        start = time.time()
        for receiver in receivers:
            gmail = Gmail()
            gmail.send(receiver, f'Scripture for {data["date"]}', f'churchPPT{data["date"]}.pptx', data["sermonTitle"])
            end = time.time()
        print("Send Mail cost：%f sec" % (end - start))

        # Done
        return f"PPT Path : {os.path.dirname(__file__)}"

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 80,debug=False)
