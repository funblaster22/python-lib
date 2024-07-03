import smtplib
import easyimap

ADDRESS = ('smtp.gmail.com', 587)
EMAIL = '***@***.com'
TARGET = '**********@txt.att.net'  # my phone
PW = ""

imapper = easyimap.connect('imap.gmail.com', EMAIL, PW)

server = smtplib.SMTP(*ADDRESS)
server.connect(*ADDRESS)
server.ehlo()
server.starttls()
server.ehlo()
server.login(EMAIL, PW)


def send(msg):
    #msg = "\nHello!"  # The /n separates the message from the headers
    server.sendmail(EMAIL, TARGET, msg)
    # server.quit()
    print('Message Sent!')


def receive():
    for mail_id in imapper.listids(limit=100):
        mail = imapper.mail(mail_id)
        if mail.from_addr == TARGET:
            '''print(mail.from_addr)
            print(mail.to)
            print(mail.cc)
            print(mail.title)
            print(mail.body)
            print(mail.attachments)'''
            print('Message Received!')
            return mail
