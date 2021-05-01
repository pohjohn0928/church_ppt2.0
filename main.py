# coding = utf-8
from Helpers.datahelper import ReadPdfFile, MakePPT
from Helpers.email import Gmail
from Helpers.docx import Word
import os
import time
from Helpers.Books import bible_config
if __name__ == '__main__':
    filename = "Calvary Bulletin 20210411.pdf"
    sermonTitle = 'Sinner, Substitute, Holy God!'
    closingSongName = 'His Name Is Wonderful - 祂名稱為奇妙 Pinyin'  # ref name : Helper/closingSong

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

    print(englishScrpitureReading["verses"])
    print(chineseScrpitureReading)
    print(englishScrpitureInSermon["verses"])
    print(chineseScrpitureInSermon)

    # englishScrpitureInSermon["verses"] = ['Leviticus 19:18', 'Leviticus 19:2', 'Leviticus 1:1-4', 'Psalm 4:4-5',
    #                                       'Psalm 4:8', 'Psalm 5:3', 'Psalm 5:7-8', 'Leviticus 1:4', '1-Peter 1:18-19',
    #                                       'Ephesians 5:1-2']
    # chineseScrpitureInSermon = ['利未記 19:18', '利未記 19:2', '詩篇 1:1-4', '詩篇 4:4-5', '詩篇 4:8', '詩篇 5:3', '詩篇 5:7-8',
    #                             '利未記 1:4', '彼得前書 1:18-19', '以弗所書 5:1-2']


    # if len(englishScrpitureReading["verses"]) != len(chineseScrpitureReading):
    #     print("englishScrpitureReading != chineseScrpitureReading")
    # elif len(englishScrpitureInSermon["verses"]) != len(chineseScrpitureInSermon):
    #     print("englishScrpitureInSermon != chineseScrpitureInSermon")
    # else:
    #     start = time.time()
    #     threads = []
    #     threads.append(MakePPT(data))
    #     threads[0].start()
    #     threads.append(Word(data))
    #     threads[1].start()
    #
    #     for t in threads:
    #         t.join()
    #     end = time.time()
    #     print(f'total cost for ppt and docx : {end - start} sec')

        # start = time.time()
        # path = os.path.join(os.path.dirname(__file__), 'Helpers/receiver/receiver.txt')
        # file = open(path)
        # for f in file:
        #     receiver = f.replace('\n', '').strip()
        #     gmail = Gmail()
        #     gmail.send(receiver,f'Scripture for {data["date"]}',f'churchPPT{data["date"]}.pptx',data["sermonTitle"])
        # end = time.time()
        # print("Send mail cost：%f sec" % (end - start))