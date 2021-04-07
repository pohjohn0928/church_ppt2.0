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


    makePPT = MakePPT(data)
    makePPT.insertScriptureData()
