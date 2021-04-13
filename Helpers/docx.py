from docx import Document
from docx.shared import Inches,Pt,RGBColor
from Helpers.datahelper import MakePPT
import threading
class Word(threading.Thread):   #threading.Thread
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.document = Document()
        date = data["date"][0:4] + '/' + data["date"][4:6] + '/' + data["date"][6:8]
        self.document.add_heading(f'Scripture for {date}', 0)

        for index in range(len(data["englishScrpitureInSermon"]["verses"])):
            scrpiture = data["englishScrpitureInSermon"]["verses"][index]
            bible_version = data["englishScrpitureInSermon"]["bibleVersion"][index]
            verse = MakePPT(data).getEnglishBibleVerses(scrpiture, bible_version)
            self.setTitle(scrpiture)
            self.setVerse(verse)
            scrpiture = data["chineseScrpitureInSermon"][index]
            verse = MakePPT(data).getChineseBibleVerses(scrpiture)
            self.setTitle(scrpiture, 'chinese')
            self.setVerse(verse, 'chinese')
        self.document.save('Scripture_In_Sermon.docx')

    def addPage(self):
        self.document.add_page_break()

    def setTitle(self,Scipture,language = 'english'):
        p = self.document.add_paragraph()
        run = p.add_run()
        run.text = Scipture
        font = run.font
        font.bold = True
        if language != 'english':
            font.name = '微軟正黑體'
        font.color.rgb = RGBColor(255, 0, 0)

    def setVerse(self,verse,language = 'english'):
        p = self.document.add_paragraph()
        for v in verse:
            v = v.replace('<start_verse>','')
            run = p.add_run()
            run.text = v
            font = run.font
            if language != 'english':
                font.name = '微軟正黑體'
