import os
from pptx import Presentation
from pptx.util import Inches, Pt,Cm
from pptx.dml.color import RGBColor
import requests
from bs4 import BeautifulSoup
from tika import parser
import pandas as pd

class ReadPdfFile:
    def __init__(self, filename):
        self.root = os.path.dirname(__file__)
        path = os.path.join(self.root, f"Bulletin/{filename}")
        parsed_pdf = parser.from_file(path)
        self.data = parsed_pdf['content']

    def getEnglishScrpitureReading(self):
        bibleVersionDic = BibleApi().bibleVersionDic
        englishBookDic = BibleApi().englishBookDic
        splitWord1 = "Today’s Scripture Reading 今日經文 "
        splitWord2 = "Scriptures in Sermon 證道經文"
        data = self.data.split(splitWord1)[1].split(splitWord2)[0]
        verses = []
        versesDic = {"verses" : [],"bibleVersion" : []}
        for info in data.split("\n"):
            for key in englishBookDic.keys():
                if key in info and len(info.rstrip()) < 25:
                    verses.append(info.rstrip())
        for verse in verses:
            hit = 0
            for key in bibleVersionDic.keys():
                if key in verse:
                    hit = 1
                    versesDic["verses"].append(verse.replace(f"({key})","").rstrip())
                    versesDic["bibleVersion"].append(key)
                    break
            if hit == 0:
                versesDic["verses"].append(verse)
                versesDic["bibleVersion"].append("NKJV")
        return versesDic

    def getChineseScrpitureReading(self):
        chineseBookDic = BibleApi().chineseBookDic
        splitWord1 = "Today’s Scripture Reading 今日經文 "
        splitWord2 = "Scriptures in Sermon 證道經文"
        data = self.data.split(splitWord1)[1].split(splitWord2)[0]
        verses = []
        for info in data.split("\n"):
            for key in chineseBookDic.keys():
                if key in info and len(info.rstrip()) < 14:
                    verses.append(info.rstrip())
        return verses

    def getEnglishScrpitureInSermon(self):
        bibleVersionDic = BibleApi().bibleVersionDic
        englishBookDic = BibleApi().englishBookDic
        splitWord1 = "Scriptures in Sermon 證道經文"
        splitWord2 = "Announcements:"
        data = self.data.split(splitWord1)[1].split(splitWord2)[0]
        versesDic = {"verses" : [],"bibleVersion" : []}
        verses = []
        for info in data.split("\n"):
            for key in englishBookDic.keys():
                if key in info:
                    otherVersion = 0
                    for keys in bibleVersionDic.keys():
                        if keys in info:
                            verses.append(info.rstrip())
                            otherVersion = 1
                    if "(See Scripture Reading)" in info:
                        verses.append(info.split("(See Scripture Reading)")[0].rstrip())
                    elif len(info.rstrip()) < 25 and otherVersion == 0:
                        verses.append(info.rstrip())

        verses = pd.unique(verses)
        for verse in verses:
            hit = 0
            for key in bibleVersionDic.keys():
                if key in verse:
                    hit = 1
                    versesDic["verses"].append(verse.replace(f"({key})","").rstrip())
                    versesDic["bibleVersion"].append(key)
                    break
            if hit == 0:
                versesDic["verses"].append(verse)
                versesDic["bibleVersion"].append("NKJV")

        return versesDic

    def getChineseScrpitureInSermon(self):
        chineseBookDic = BibleApi().chineseBookDic
        splitWord1 = "Scriptures in Sermon 證道經文"
        splitWord2 = "Announcements:"
        data = self.data.split(splitWord1)[1].split(splitWord2)[0]
        verses = []
        for info in data.split("\n"):
            for key in chineseBookDic.keys():
                if key in info:
                    if "(詳見今日經文)" in info:
                        verses.append(info.split(" ")[0] + " " + info.split(" ")[1])
                    elif len(info.rstrip()) < 14:
                        verses.append(info.rstrip())
        return verses

    def getClosingSong(self,closingSongName):
        path = os.path.join(self.root,f'closingSong/{closingSongName}.txt')
        try:
            file = open(path,encoding='utf-8')
            lyrics = ""
            for f in file:
                lyrics += f
            closingSong_chinese = lyrics.split('(English)')[0].split('\n')
            closingSong_english = lyrics.split('(English)')[1].split('\n')
            del closingSong_chinese[-1]
            del closingSong_english[0]
            closingSong = {"closingSong_chinese":closingSong_chinese,"closingSong_english" : closingSong_english}
            return closingSong
        except:
            print("Can't find out the closingSongName !")

    def getBlessingSong(self):
        path = self.root + '/blessingSong/blessing_song.txt'
        file = open(path)
        blessing_song = []
        for lyrics in file:
            blessing_song.append(lyrics.replace('\n',''))
        return blessing_song

class BibleApi:
    def __init__(self):
        root = os.path.dirname(__file__)
        self.bibleVersion = root + "/bibleVersion/bibleVersion.txt"
        self.englishBook = root + "/Books/englishBook.txt"
        self.chineseBook = root + "/Books/chineseBook.txt"
        self.setBibleVersion()
        self.setEnglishBook()
        self.setChineseBook()
        self.englishVerseBaseUrl = "https://biblia-api-pdf.herokuapp.com/api?method=bible&"
        self.chineseVerseBaseUrl = "http://ibibles.net/quote.php?cut-"

    # def getEnglishVerse(self,bibleVersion,book,chapter,startVerse,endVerse):
    #     url = self.englishVerseBaseUrl + f"version={bibleVersion}&book={book}&cStart={chapter}&cEnd={chapter}&vStart={startVerse}&vEnd={endVerse}"
    #     r = requests.get(url)
    #     print(url)
    #     verses = r.json()["content"][0]["verses"]
    #     return_verses = []
    #     startVerse = int(startVerse)
    #     endVerse = int(endVerse)
    #     for verse in verses:
    #         content = verses[f"v{startVerse}"]
    #         content = f"<start_verse>{startVerse} " + content
    #         return_verses.append(content)
    #         startVerse += 1
    #     return return_verses

    def getEnglishVerse(self,bibleVersion,book,chapter,startVerse,endVerse):
        startVerse = int(startVerse)
        endVerse = int(endVerse)
        return_verses = []
        response = requests.get(f"https://www.biblestudytools.com/{bibleVersion}/{book}/{chapter}.html")
        soup = BeautifulSoup(response.text, "html.parser")

        for i in range(startVerse,endVerse + 1):
            result = soup.find("span", class_=f"verse-{i}")
            return_verses.append(f"<start_verse>{i} {result.text.strip()}")
        return return_verses


    def getChineseVerse(self,book,chapter,startVerse,endVerse):
        url = self.chineseVerseBaseUrl + f"{book}/{chapter}:{startVerse}-{endVerse}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return_verses = soup.find('body').get_text().split('\n')
        return_verses = ["<start_verse>" + verse for verse in return_verses if verse != ""]
        # return_verses = [" ".join(verse.split(" ")[1:]) for verse in return_verses if verse != ""]

        return return_verses


    def setBibleVersion(self):
        self.bibleVersionDic = {}
        file = open(self.bibleVersion)
        for bibleVersion in file:
            self.bibleVersionDic[bibleVersion.replace("\n","").split(",")[0]] = bibleVersion.replace("\n","").split(",")[1]

    def setEnglishBook(self):
        self.englishBookDic = {}
        file = open(self.englishBook)
        for book in file:
            self.englishBookDic[book.replace("\n","").split(" ",2)[2]] = book.replace("\n","").split(" ",2)[1]


    def setChineseBook(self):
        self.chineseBookDic = {}
        file = open(self.chineseBook,"r",encoding="utf-8")
        for book in file:
            self.chineseBookDic[book.replace("\n","").split(" ")[1]] = book.replace("\n","").split(" ")[0]


class MakePPT:
    def __init__(self, data):
        self.prs = Presentation()
        self.prs.slide_width = Inches(16)
        self.prs.slide_height = Inches(9)
        self.data = data
        self.word_limit = 68
        self.word_limit_chinese = 155
        self.layout = self.prs.slide_layouts[6]
        self.start_verse_token = "<start_verse>"

    def insertScriptureData(self):
        englishScrpitureReading = self.data["englishScrpitureReading"]
        chineseScrpitureReading = self.data["chineseScrpitureReading"]
        englishScrpitureInSermon = self.data["englishScrpitureInSermon"]
        chineseScrpitureInSermon = self.data["chineseScrpitureInSermon"]
        self.addCalvaryImg()
        self.addAnnocement()
        self.representAtPPTScrpitureReading(englishScrpitureReading)
        self.representAtPPTScrpitureReading(chineseScrpitureReading,'chinese')
        self.addCalvaryImg()
        self.representAtPPTScrpitureInSermon(englishScrpitureInSermon,chineseScrpitureInSermon)
        self.addCalvaryImg()
        self.addClosingSong()
        self.addCalvaryImg()
        self.addBlessingSong()
        self.addCalvaryImg()
        self.prs.save(f'churchPPT{self.data["date"]}.pptx')

    def addAnnocement(self):
        if self.data['annocement'] == []:
            pass

        else:
            for annoce in self.data['annocement']:
                img_path = os.path.dirname(__file__) + f'/annocement/{annoce}.png'
                slide = self.prs.slides.add_slide(self.layout)
                top = Inches(0)
                left = Inches(0)
                height = Inches(9)
                slide.shapes.add_picture(img_path, left, top, height=height)
            self.addCalvaryImg()

    def representAtPPTScrpitureReading(self,info,language = 'english'):
        if language == 'english':
            ScrpitureInSermon_title_slide_layout = self.prs.slide_layouts[0]
            slide = self.prs.slides.add_slide(ScrpitureInSermon_title_slide_layout)
            title = slide.shapes.title

            title.width = Cm(40)
            title.top = Inches(4)
            title.text = "Scrpiture Reading"
            title.text_frame.paragraphs[0].font.size = Pt(60)
            for index in range(len(info["verses"])):
                scripture = info["verses"][index]
                bibleVersion = info["bibleVersion"][index]
                verses = self.getEnglishBibleVerses(scripture,bibleVersion)
                self.addPage(scripture,verses)
        else:
            for scripture in info:
                verses = self.getChineseBibleVerses(scripture)
                self.addPage(scripture,verses,'chinese')

    def representAtPPTScrpitureInSermon(self,englishScrpitureInSermon,chineseScrpitureInSermon):
        englishVerses = []
        chineseVerses = []
        for index in range(len(englishScrpitureInSermon["verses"])):
            scripture = englishScrpitureInSermon["verses"][index]
            bibleVersion = englishScrpitureInSermon["bibleVersion"][index]
            verses = self.getEnglishBibleVerses(scripture,bibleVersion)
            if verses == None:
                verses = ["None"]
            englishVerses.append(verses)
        for chineseScrpiture in chineseScrpitureInSermon:
            verses = self.getChineseBibleVerses(chineseScrpiture)
            chineseVerses.append(verses)

        ScrpitureInSermon_title_slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(ScrpitureInSermon_title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = "Sermon Title"
        title.width = Cm(40)
        title.top = Inches(4)
        subtitle.text = self.data["sermonTitle"]
        subtitle.width = Cm(40)
        subtitle.top = Inches(5)
        title.text_frame.paragraphs[0].font.size = Pt(60)
        subtitle.text_frame.paragraphs[0].font.size = Pt(50)
        for i in range(len(englishScrpitureInSermon["verses"])):
            slide = self.prs.slides.add_slide(self.layout)
            tf = self.initTxBox(slide)
            self.setChapter(tf,englishScrpitureInSermon["verses"][i])
            pageContent = self.seperateVerse(englishVerses[i])
            p = tf.add_paragraph()
            run = p.add_run()
            if len(pageContent) == 1:
                self.represent_verse_in_ppt(pageContent[0],p)
            else:
                for index in range(len(pageContent)):
                    if index == 0:
                        self.represent_verse_in_ppt(pageContent[0],p)
                    else:
                        self.addNewPageToFinishTheRest(pageContent[index])
            font = run.font
            font.size = Pt(54)

            slide = self.prs.slides.add_slide(self.layout)
            tf = self.initTxBox(slide)
            self.setChapter(tf,chineseScrpitureInSermon[i],'chinese')
            pageContent = self.seperateVerse(chineseVerses[i],'chinese')
            p = tf.add_paragraph()
            run = p.add_run()
            if len(pageContent) == 1:
                self.represent_verse_in_ppt(pageContent[0],p,'chinese')
            else:
                for index in range(len(pageContent)):
                    if index == 0:
                        self.represent_verse_in_ppt(pageContent[0], p, 'chinese')
                        content = pageContent[0].split(self.start_verse_token)
                    else:
                        self.addNewPageToFinishTheRest(pageContent[index],'chinese')
            font = run.font
            font.name = '微軟正黑體'
            font.size = Pt(54)

    def initTxBox(self,slide):
        left = top = Inches(0.3)  # 位置
        width = Inches(15)  # 大小
        height = Inches(8)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        return tf

    def setChapter(self,tf,chapter,language = 'english'):
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = chapter
        font = run.font
        font.size = Pt(54)
        font.bold = True
        if language == 'chinese':
            font.name = '微軟正黑體'
        font.color.rgb = RGBColor(255, 0, 0)

    def addPage(self,scripture,verses,language = 'english'):
        slide = self.prs.slides.add_slide(self.layout)
        tf = self.initTxBox(slide)
        self.setChapter(tf,scripture,language)
        p = tf.add_paragraph()

        run = p.add_run()
        pageContent = self.seperateVerse(verses,language)
        if len(pageContent) == 1:
            content = pageContent[0].split(self.start_verse_token)
            for c in content:
                if c != '':
                    scr = c.split(" ")[0]
                    verse = " ".join(c.split(" ")[1:])
                    self.show_content(scr,p,True,language)
                    self.show_content(verse,p,False,language)
        else:
            for index in range(len(pageContent)):
                if index == 0:
                    content = pageContent[index].split(self.start_verse_token)
                    for c in content:
                        if c != '':
                            scr = c.split(" ")[0]
                            verse = " ".join(c.split(" ")[1:])
                            self.show_content(scr, p, True, language)
                            self.show_content(verse, p, False, language)
                else:
                    self.addNewPageToFinishTheRest(pageContent[index],language)
        font = run.font

        if language == 'chinese':
            font.name = '微軟正黑體'
        font.size = Pt(54)


    def addNewPageToFinishTheRest(self,content,language = 'english'):
        slide = self.prs.slides.add_slide(self.layout)
        tf = self.initTxBox(slide)

        p = tf.paragraphs[0]
        content = content.split(self.start_verse_token)
        if content[0] == '':
            for c in content:
                if c != '':
                    scr = c.split(" ")[0]
                    verse = " ".join(c.split(" ")[1:])
                    self.show_content(scr, p, True, language)
                    self.show_content(verse, p, False, language)
        else:
            self.show_content(content[0], p, False, language)
            for index in range(1,len(content)):
                scr = content[index].split(" ")[0]
                verse = " ".join(content[index].split(" ")[1:])
                self.show_content(scr, p, True, language)
                self.show_content(verse, p, False, language)

    def seperateVerse(self,verses,language = 'english'):
        contentEachPage = []
        i = 0
        block = ""
        if language == 'english':
            for index in range(len(verses)):
                words = verses[index].split(" ")
                for word in words:
                    block += word + " "
                    i += 1
                    if i % self.word_limit == 0:
                        contentEachPage.append(block)
                        block = ''
        else:
            for index in range(len(verses)):
                for word in verses[index]:
                    block += word
                    i += 1
                    if i % self.word_limit_chinese == 0:
                        contentEachPage.append(block)
                        block = ''
        contentEachPage.append(block)
        return contentEachPage

    def represent_verse_in_ppt(self,content,p,language = 'english'):
        content = content.split(self.start_verse_token)
        if content[0] == '':
            for c in content:
                if c != '':
                    scr = c.split(" ")[0]
                    verse = " ".join(c.split(" ")[1:])
                    self.show_content(scr, p, True, language)
                    self.show_content(verse, p, False, language)

    def set_superscript(self,font):
        font._element.set('baseline', '30000')

    def show_content(self,content,p,superscript = False,language = 'english'):
        run = p.add_run()
        run.text = content
        font = run.font
        font.size = Pt(54)
        if language == 'chinese':
            font.name = '微軟正黑體'
        if superscript:
            self.set_superscript(font)

    def getEnglishBibleVerses(self,scripture,bibleVersion):
        bibleApi = BibleApi()
        englishBookDic = bibleApi.englishBookDic
        for key in englishBookDic.keys():
            if key in scripture:
                # book = englishBookDic[key]
                book = key
                chapter = scripture.split(" ")[-1].split(":")[0]
                verses = scripture.split(" ")[-1].split(":")[1].split("-")
                startVerse = scripture.split(" ")[-1].split(":")[1].split("-")[0]
                endVerse = startVerse
                if len(verses) != 1:
                    endVerse = scripture.split(" ")[-1].split(":")[1].split("-")[1]
        try:
            return bibleApi.getEnglishVerse(bibleVersion,book,chapter,startVerse,endVerse)
        except:
            pass

    def getChineseBibleVerses(self,info):
        bibleApi = BibleApi()
        chineseBookDic = bibleApi.chineseBookDic
        for key in chineseBookDic.keys():
            if key in info:
                book = chineseBookDic[key]
                chapter = info.split(" ")[-1].split(":")[0]
                verses = info.split(" ")[-1].split(":")[1].split("-")
                startVerse = info.split(" ")[-1].split(":")[1].split("-")[0]
                endVerse = startVerse
                if len(verses) != 1:
                    endVerse = info.split(" ")[-1].split(":")[1].split("-")[1]
        return bibleApi.getChineseVerse(book,chapter,startVerse,endVerse)

    def addClosingSong(self):
        closingSong_slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(closingSong_slide_layout)
        title = slide.shapes.title
        title.text = self.data["closingSongName"]
        title.width = Cm(40)
        title.top = Inches(4)
        title.text_frame.paragraphs[0].font.size = Pt(60)

        try:
            closingSong = self.data["closingSong"]
            content = ""
            contentList = []
            for index in range(len(closingSong["closingSong_chinese"])):
                content += closingSong["closingSong_chinese"][index] + '\n'
                if (index + 1) % 6 == 0:
                    contentList.append(content)
                    content = ""


            contentList.append(content)
            for lyrics in contentList:
                if lyrics != '':
                    self.addNewPageToFinishTheRest(lyrics,'chinese')

            content = ""
            contentList = []
            for index in range(len(closingSong["closingSong_english"])):
                content += closingSong["closingSong_english"][index] + '\n'
                if (index + 1) % 8 == 0:
                    contentList.append(content)
                    content = ""

            contentList.append(content)
            for lyrics in contentList:
                if lyrics != '' and lyrics != '\n':
                    self.addNewPageToFinishTheRest(lyrics)
        except:
            pass


    def addBlessingSong(self):
        blessingSong_slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(blessingSong_slide_layout)
        title = slide.shapes.title
        title.text = "The Blessing Song"
        title.width = Cm(40)
        title.top = Inches(4)
        title.text_frame.paragraphs[0].font.size = Pt(60)

        blessing_song = self.data["blessing_song"]
        contentInFirstPage = []
        contentInSecondPage = []
        for i in range(len(blessing_song)):
            if i <= 6 :
                contentInFirstPage.append(blessing_song[i])
            else:
                contentInSecondPage.append(blessing_song[i])

        slide = self.prs.slides.add_slide(self.layout)
        tf = self.initTxBox(slide)
        p = tf.paragraphs[0]
        run = p.add_run()
        for lyrics in contentInFirstPage:
            run.text += lyrics + '\n'
        font = run.font
        font.size = Pt(60)

        slide = self.prs.slides.add_slide(self.layout)
        tf = self.initTxBox(slide)
        p = tf.paragraphs[0]
        run = p.add_run()
        for lyrics in contentInSecondPage:
            run.text += lyrics + '\n'
        font = run.font
        font.size = Pt(60)


    def addCalvaryImg(self):
        img_path = os.path.dirname(__file__) + '/Img/calvary.png'
        slide = self.prs.slides.add_slide(self.layout)
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0, 0, 0)
        top = Inches(0)
        left = Inches(2)
        height = Inches(9)
        slide.shapes.add_picture(img_path, left, top,height=height)

