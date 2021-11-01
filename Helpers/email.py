from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os


class Gmail:
    def __init__(self):
        self.content = MIMEMultipart()
        self.token = 'oaumeytzfyeklkbp'
        self.sender = 'pohjohn0928@gmail.com'
        self.content["from"] = self.sender
        self.smtp = smtplib.SMTP(host="smtp.gmail.com", port="587")
        self.root = os.path.dirname(__file__)

    def send(self,receiver, title, file_path, sermon_title):
        self.content["to"] = receiver
        self.content["subject"] = title
        self.content.attach(MIMEText(f'Sermon Title : {sermon_title}'))
        self.sendfile(file_path)
        self.sendfile('Scripture_In_Sermon.docx')
        try:
            self.smtp.ehlo()  # 驗證SMTP伺服器
            self.smtp.starttls()  # 建立加密傳輸
            self.smtp.login(self.sender, self.token)
            self.smtp.sendmail(self.sender, receiver, self.content.as_string())
            self.smtp.close()
            print(f'Mail Sent to \'{receiver}\'')
        except Exception as e:
            print("Error message: ", e)

    def sendfile(self, file_path):
        attach_file_name = file_path
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attach_file_name, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach_file_name))
        self.content.attach(part)
