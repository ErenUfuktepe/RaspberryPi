import smtplib
import imaplib
import configparser
import pandas as pd
from email.message import EmailMessage
import email
from email.header import decode_header
from datetime import datetime
import datetime as dt

def remind(subject, body, user, to, password):
	message = EmailMessage()
	message.set_content(body)
	message['subject'] = subject
	message['from'] = user
	message['to'] = to
	
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(message)
	
	server.quit()


def delete_all_emails(username, password):
	imap = imaplib.IMAP4_SSL("imap.gmail.com")
	imap.login(username, password)
	imap.select("INBOX")
	status, messages = imap.search(None, "ALL")
	messages = messages[0].split(b' ')
	for mail in messages:
		_, msg = imap.fetch(mail, "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
		imap.store(mail, "+FLAGS", "\\Deleted")
	imap.close()
	imap.logout()
	

def check_and_read_email(username, password, target):
	result = str()
	imap = imaplib.IMAP4_SSL("imap.gmail.com")
	imap.login(username, password)
	status, messages = imap.select("INBOX")
	
	messages = int(messages[0])
	if messages == 0:
		result = "empty"
	else:
		res, msg = imap.fetch(str(messages), "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				From, encoding = decode_header(msg.get("From"))[0]
				if isinstance(From, bytes):
					From = From.decode(encoding)
				if target == From:
					if msg.is_multipart():
						for part in msg.walk():
							content_type = part.get_content_type()
							content_disposition = str(part.get("Content-Disposition"))
							try:
								body = part.get_payload(decode=True).decode()
							except:
								pass
							if content_type == "text/plain" and "attachment" not in content_disposition:
								result = body
					else:
						content_type = msg.get_content_type()
						body = msg.get_payload(decode=True).decode()
						if content_type == "text/plain":
							result = body
				else:
					result = "empty"
	imap.close()
	imap.logout()
	return result
    

def today_calender(df, date):
    remind_today = df[df['Date']==date]
    tasks = remind_today.shape[0]
    myString = ''
    if tasks > 0:
        for index in remind_today.index:
            myString = str(index) + '.' + remind_today['Subject'][index] + ' - ' + remind_today['Description'][index] + '\n' + myString
    body = '\nToday you have ' + str(tasks) + ' reminder!\n' + myString
    remind('Good Morning Eren', body, username, target, password)
    return remind_today

def listen_and_remind(temp_df, date):
    response = check_and_read_email(username, password, target)
    while not temp_df[temp_df['Date'] == date].shape[0] == 0:
        response = check_and_read_email(username, password, target)
        while not response == 'empty':
            #read, parse, update
            reponse = reponse.split('-')
            if response[1] == 'Done':
                df.loc[df['Description'] == response[0],'Date'] = update_date(df.loc[df['Description'] == response[0],'Date']['Repetition'].iloc[0],
                                                                              df.loc[df['Description'] == response[0],'Date']['Date'].iloc[0])
                temp_df = temp_df[temp_df['Description'] != response[0]]
            delete_all_emails(username, password)
        #sleep and remind


def update_date(repetition, old_date):
    old = old_date.split('-')
    result = str()
    if repetition == 'Yearly':
        result = str(datetime(now.year + 1, int(old[1]), int(old[2]))).split(' ')[0]
    elif repetition == 'Monthly':
        check_month = int(old[1]) + 1
        check_year = int(old[0])
        if check_month > 12:
            check = 1
            check_year = check_year + 1
        result = str(datetime(check_year, check_month, int(old[2]))).split(' ')[0]
    elif repetition == 'Daily':
        result = str(datetime(int(old[0]), int(old[1]), int(old[2])) + dt.timedelta(days=1)).split(' ')[0]
    return result

def testt():
    print(date)

configParser = configparser.RawConfigParser()
configParser.read('private_settings.config') # change it with your config file name.
username = configParser.get('Default', 'email')
password = configParser.get('Default', 'password')
target = configParser.get('Default', 'target')

test = True

df = pd.read_csv('notes.csv') # Change it with your file name.
temp_df = None

now = datetime.now()
today = str(now).split(' ')
time = today[1].split(':')
date = today[0]

if not test:
    while True:
        try:
            now = datetime.now()
            today = str(now).split(' ')
            time = today[1].split(':')
            date = today[0]
            if int(time[0]) == 9:
                temp_df = today_calender(df, date)
                if temp_df.shape[0] > 0:
                    listen_and_remind(temp_df)                  
        except:
            remind('System error!', 'Program terminated!', username, target, password)
else:
    print('end')
