import requests
import re
import csv
import smtplib
import sqlite3
from email.mime.text import MIMEText

def send_email(email, names_list):
   msg = MIMEText(str(names_list))
   msg['Subject'] = 'Death notice update'
   msg['From'] = 'max.flander@gmail.com'
   msg['To'] = 'max.flander@gmail.com'
   #generate these credentials in the AWS SES console
   user = 'AKIAJ6T4GKNA2RSC5BLA'
   password = 'Aphr4KHqMF5a9g0828aoK+xFf8iNjvn9zW2XvadvEFSX'
   s = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com')
   s.starttls()
   s.login(user,password)
   s.sendmail(msg['From'], msg['To'], msg.as_string())
   s.quit()

db = sqlite3.Connection('watchlist')
db.execute("create table watchlist (email varchar(30),  firstname varchar(30), lastname varchar(30))")
db.execute("create table todays_deaths (surname varchar(200), firstnames varchar(200), source varchar (20))")
with open('watchlist.txt') as f:
   reader = csv.reader(f)
   for line in reader:
      db.execute("insert into watchlist values ('{}','{}','{}')".format(*line))


theage = 'http://tributes.theage.com.au/obituaries/theage-au/obituary-browse.aspx?&page=1&entriesperpage=10&view=1&from=scroll&date=pastweek'
data=requests.get(theage).text
#names in the html look like: <span class="Name">Griffith,  Edwin Alexander</span>
name_regex = re.compile('<span class="Name">([^\<]+)')
names = name_regex.findall(data)

for line in names:
   print(line)
   db.execute("insert into todays_deaths values ('{}','{}','The Age')".format(*[s.strip() for s in line.lower().replace("'","''").split(',')]))

#(lastname:smith, firstname:tom) in the watchlist matches
#(lastname:smith, firstname:"john tommy") in todays deaths

query = """select distinct email, w.firstname||' '||w.lastname, source from todays_deaths t
           join watchlist w
           on lower(t.surname) = lower(w.lastname)
           and lower(t.firstnames) like '%'||lower(w.firstname)||'%'"""
matches = db.execute(query).fetchall()

for match in matches:
   send_email(match[0], "Hopefully its the wrong person but we found a match for {} in {}".format(match[1],match[2]))
