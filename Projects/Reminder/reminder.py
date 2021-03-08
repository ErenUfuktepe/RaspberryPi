import smtplib
import imaplib
import configparser
from email.message import EmailMessage
import email
from email.header import decode_header


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
	status, messages = imap.search(None, "ALL")
	messages = messages[0].split(b' ')
	for mail in messages:
		_, msg = imap.fetch(mail, "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				# decode the email subject
				subject = decode_header(msg["Subject"])[0][0]
				if isinstance(subject, bytes):
					# if it's a bytes type, decode to str
					subject = subject.decode()
				print("Deleting", subject)
		imap.store(mail, "+FLAGS", "\\Deleted")
	imap.close()
	imap.logout()
	

def check_and_read_email(username, password, target):
	result = str()
	imap = imaplib.IMAP4_SSL("imap.gmail.com")
	imap.login(username, password)
	status, messages = imap.select("INBOX")
	
	messages = int(messages[0])
	print(messages)
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

configParser = configparser.RawConfigParser()
configParser.read('private_settings.config') # change it with your config file name.
username = configParser.get('Default', 'email')
password = configParser.get('Default', 'password')
target = configParser.get('Default', 'target')

#print(username)
#print(password)
#print(check_and_read_email(username, password, target))
