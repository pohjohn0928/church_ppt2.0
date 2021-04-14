# coding = utf-8
from Helpers.datahelper import ReadPdfFile, MakePPT
from Helpers.email import Gmail
from Helpers.docx import Word
import os
import time
if __name__ == '__main__':
    filename = "Calvary Bulletin 20210411.pdf"
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

    # englishScrpitureReading = {'verses': ['Mark 16:8', 'Mark 4:39-41', 'Luke 23:40-41'],
    #                            'bibleVersion': ['NKJV', 'NKJV', 'NKJV']}
    # chineseScrpitureReading = ['馬可福音 16:8', '馬可福音 4:39-41', '路加福音 23:40-41']
    # englishScrpitureInSermon = {
    #     'verses': ['Proverbs 6:6', 'Mark 16:8', 'Mark 1:1', 'Mark 4:39-41', 'Mark 5:32-33', 'Mark 15:43',
    #                'John 19:39-40', 'Matthew 7:21-23', 'Luke 23:40-41'],
    #     'bibleVersion': ['NKJV', 'NKJV', 'NKJV', 'NKJV', 'NKJV', 'ESV', 'NKJV', 'NKJV', 'NKJV']}
    # chineseScrpitureInSermon = ['箴言 6:6', '馬可福音 16:8', '馬可福音 1:1', '馬可福音 4:39-41', '馬可福音 5:32-33', '馬可福音 15:43',
    #                             '約翰福音 19:39-40', '馬太福音 7:21-23', '路加福音 23:40-41']

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

        start = time.time()
        path = os.path.join(os.path.dirname(__file__), 'Helpers/receiver/receiver.txt')
        file = open(path)
        for f in file:
            receiver = f.replace('\n', '').strip()
            gmail = Gmail()
            gmail.send(receiver,f'Scripture for {data["date"]}',f'churchPPT{data["date"]}.pptx',data["sermonTitle"])
        end = time.time()
        print("Send mail cost：%f sec" % (end - start))