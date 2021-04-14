from flask import Flask, request, render_template
from Helpers.datahelper import ReadPdfFile, MakePPT
from Helpers.docx import Word
from Helpers.email import Gmail
import time

import os
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/getPdfFile', methods=["POST"])
def getPdfFile():
    filename = request.values['pdf_name']
    sermonTitle = request.values['sermon_title']
    closingSongName = request.values['closing_song']
    annocement = request.form.get('annocement')
    annocement = json.loads(annocement)["annocement"]
    readPdfFile = ReadPdfFile(filename)
    englishScrpitureReading = readPdfFile.getEnglishScrpitureReading()
    chineseScrpitureReading = readPdfFile.getChineseScrpitureReading()
    englishScrpitureInSermon = readPdfFile.getEnglishScrpitureInSermon()
    chineseScrpitureInSermon = readPdfFile.getChineseScrpitureInSermon()

    closingSong = readPdfFile.getClosingSong(closingSongName)
    blessing_song = readPdfFile.getBlessingSong()
    date = filename.split(" ")[2].split('.')[0]

    data = {"annocement": annocement, "englishScrpitureReading": englishScrpitureReading,
            "chineseScrpitureReading": chineseScrpitureReading, "englishScrpitureInSermon": englishScrpitureInSermon,
            "chineseScrpitureInSermon": chineseScrpitureInSermon, "sermonTitle": sermonTitle, "date": date,
            "closingSongName": closingSongName, "closingSong": closingSong, "blessing_song": blessing_song}

    if len(englishScrpitureReading["verses"]) != len(chineseScrpitureReading):
        return 'Error'
    elif len(englishScrpitureInSermon["verses"]) != len(chineseScrpitureInSermon):
        return 'Error'
    else:
        Word(data)

        makePPT = MakePPT(data)
        makePPT.insertScriptureData()

        path = os.path.join(os.path.dirname(__file__), 'Helpers/receiver/receiver.txt')
        file = open(path)

        start = time.time()
        for f in file:
            receiver = f.replace('\n', '').strip()
            gmail = Gmail()
            gmail.send(receiver, f'Scripture for {data["date"]}', f'churchPPT{data["date"]}.pptx', data["sermonTitle"])
            end = time.time()
        print("Send Mail cost：%f sec" % (end - start))
        return f"PPT Path : {os.path.dirname(__file__)}"



if __name__ == '__main__':
    app.run(debug=True)
