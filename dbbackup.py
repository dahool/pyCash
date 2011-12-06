#!/usr/bin/python
import sys
import os
import tarfile
import time
import datetime

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJECT_PATH)
import settings

SENDMAIL = "/usr/sbin/sendmail" 
MYSQLDUMP = "/usr/bin/mysqldump"

    DATABASES = {
        'default': {
            'NAME': 'expenses',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '',
        },
    }
    
    
username = settings.DATABASES['DEFAULT']['USER']
password = settings.DATABASES['DEFAULT']['PASSWORD']
database = settings.DATABASES['DEFAULT']['NAME']
host = settings.DATABASES['DEFAULT']['HOST']

if host == '':
    host = 'localhost'
    
path = '/tmp'

os.chdir(path)

filename = database + "_" + datetime.datetime.now().strftime('%Y%m%d%H%M') + ".sql"

print "Creating %s\n" % filename

#command = MYSQLDUMP + " --user=" + username + " --password=" + password + " -B " + database + " -h " + host + " --add-drop-table -c -C -e -K -n --add-locks -q --result-file=" + filename
command = MYSQLDUMP + " --user=" + username + " --password=" + password + " -h " + host + " --add-drop-table -c -C -e -K -n --add-locks -q --result-file=" + filename + " " + database
os.system(command)

print "Compressing\n"

tarname = filename + ".tar.gz"
tar = tarfile.open(tarname,"w:gz")
tar.add(filename);
tar.close();

os.remove(filename)

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def sendMail(to, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list
    fro = "pyCash <gabriel@titan.sgt>"

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        fo = open(file,"rb")
        part.set_payload( fo.read() )
        fo.close()
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

sendMail(
        ["gabriel.sgt@gmail.com"],
        "PYCASH BACKUP [" + filename + "]","",
        [tarname]
    )
time.sleep(5)
os.remove(tarname)
