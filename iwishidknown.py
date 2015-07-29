import requests
import re
import csv
import smtplib
from email.mime.text import MIMEText

def send_email(email, names_list):
   msg = MIMEText(str(names_list))
   msg['Subject'] = 'Death notice update'
   msg['From'] = 'max.flander@gmail.com'
   msg['To'] = 'max.flander@gmail.com'

   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login("max.flander@gmail.com", "actqrbqxwsnknhip")
   server.send_message(msg)
   server.quit()


watchlist = []
with open('/Users/maxflander/Dropbox/1.txt') as f:
   reader = csv.reader(f)
   for line in reader:
      line = [l.lower() for l in line]
      watchlist.append({'email':line[0],'firstname':line[1],'lastname':line[2]})

theage = 'http://tributes.theage.com.au/obituaries/theage-au/obituary-browse.aspx?&page=1&entriesperpage=10&view=1&from=scroll&date=yesterday'
data=requests.get(theage).text
name_regex = re.compile('<span class="Name">([^\<]+)')
names = name_regex.findall(data)

todays_names = []
for line in names:
   line = line.lower().split(',')
   todays_names.append({'lastname':line[0].strip(), 'firstnames':line[1].strip(),'source':'The Age'})

matches = {}
for watcher in watchlist:
   for name in todays_names:
      if watcher['lastname'] == name['lastname'] and watcher['firstname'] in name['firstnames']:
         if watcher['email'] not in matches: matches[watcher['email']] = []
         matches[watcher['email']].append(name)
         
   
for email, L in matches.items():
   send_email(mail, L)
   