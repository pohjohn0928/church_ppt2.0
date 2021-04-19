# coding = utf-8
from Helpers.datahelper import ReadPdfFile, MakePPT
from Helpers.email import Gmail
from Helpers.docx import Word
import os
import time
if __name__ == '__main__':
    filename = "Calvary Bulletin 20210418.pdf"
    sermonTitle = 'Afraid? Fearful? Enter the Kingdom of God!'
    closingSongName = 'Amazing Grace - 奇異恩典'  # ref name : Helper/closingSong

    readPdfFile = ReadPdfFile(filename)

    englishScrpitureReading = readPdfFile.getEnglishScrpitureReading()
    chineseScrpitureReading = readPdfFile.getChineseScrpitureReading()
    englishScrpitureInSermon = readPdfFile.getEnglishScrpitureInSermon()
    chineseScrpitureInSermon = readPdfFile.getChineseScrpitureInSermon()
    closingSong = readPdfFile.getClosingSong(closingSongName)
    blessing_song = readPdfFile.getBlessingSong()
    date = filename.split(" ")[2].split('.')[0]

    data = {"annocement": [], "englishScrpitureReading": englishScrpitureReading,
            "chineseScrpitureReading": chineseScrpitureReading,
            "englishScrpitureInSermon": englishScrpitureInSermon, "chineseScrpitureInSermon": chineseScrpitureInSermon,
            "sermonTitle": sermonTitle, "date": date, "closingSongName": closingSongName, "closingSong": closingSong,
            "blessing_song": blessing_song}

    if len(englishScrpitureReading["verses"]) != len(chineseScrpitureReading):
        print("englishScrpitureReading != chineseScrpitureReading")
    elif len(englishScrpitureInSermon["verses"]) != len(chineseScrpitureInSermon):
        print("englishScrpitureInSermon != chineseScrpitureInSermon")

    else:
        start = time.time()
        threads = []
        threads.append(MakePPT(data))
        threads[0].start()
        threads.append(Word(data))
        threads[1].start()

        for t in threads:
            t.join()
        end = time.time()
        print(f'total cost for ppt and docx : {end - start} sec')

    #     start = time.time()
    #     path = os.path.join(os.path.dirname(__file__), 'Helpers/receiver/receiver.txt')
    #     file = open(path)
    #     for f in file:
    #         receiver = f.replace('\n', '').strip()
    #         gmail = Gmail()
    #         gmail.send(receiver,f'Scripture for {data["date"]}',f'churchPPT{data["date"]}.pptx',data["sermonTitle"])
    #     end = time.time()
    #     print("Send mail cost：%f sec" % (end - start))