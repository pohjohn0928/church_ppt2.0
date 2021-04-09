# coding=utf-8
from Helpers.datahelper import ReadPdfFile, MakePPT


if __name__ == '__main__':
    filename = "Calvary Bulletin 20210307.pdf"
    sermonTitle = 'Believe in Jesus first,Then you will See'
    closingSongName = 'His Name Is Wonderful - 祂名稱為奇妙 Pinyin' # ref name : Helper/closingSong

    readPdfFile = ReadPdfFile(filename)

    englishScrpitureReading = readPdfFile.getEnglishScrpitureReading()
    chineseScrpitureReading = readPdfFile.getChineseScrpitureReading()
    englishScrpitureInSermon = readPdfFile.getEnglishScrpitureInSermon()
    chineseScrpitureInSermon = readPdfFile.getChineseScrpitureInSermon()
    closingSong = readPdfFile.getClosingSong(closingSongName)
    blessing_song = readPdfFile.getBlessingSong()
    date = filename.split(" ")[2].split('.')[0]
    data = {"annocement" : [],"englishScrpitureReading": englishScrpitureReading, "chineseScrpitureReading": chineseScrpitureReading,
            "englishScrpitureInSermon": englishScrpitureInSermon, "chineseScrpitureInSermon": chineseScrpitureInSermon,
            "sermonTitle": sermonTitle, "date": date,"closingSongName" : closingSongName,"closingSong" : closingSong ,"blessing_song": blessing_song}

    # data['englishScrpitureReading'] = {'verses': ['Mark 15:6-12', 'John 1:29', 'Isaiah 53:7'], 'bibleVersion': ['NKJV', 'NKJV', 'NKJV']}
    # chineseScrpitureReading = ['馬可福音 15:6-12', '約翰福音 1:29', '以賽亞書 53:7']
    # englishScrpitureInSermon = {'verses': [],'bibleVersion': []}
    # chineseScrpitureInSermon = []

    if len(englishScrpitureReading["verses"]) != len(chineseScrpitureReading):
        print("Error")
    elif len(englishScrpitureInSermon["verses"]) != len(chineseScrpitureInSermon):
        print("Error")
    else:
        makePPT = MakePPT(data)
        makePPT.insertScriptureData()
