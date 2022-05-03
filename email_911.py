import serial
import numpy as np
import sys
import imghdr

import smtplib, ssl
from email.mime.base import MIMEBase 
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from os.path import basename
from email import encoders
from datetime import  datetime



def email_emergency(pic_num):
	path = "./cap_pics/" + str(pic_num) + ".jpg"
	print('firing email')
	port=465	            
	context = ssl.create_default_context()
	EMAIL_ADDRESS = 'coverletterwriter@gmail.com'
	EMAIL_PASSWORD = 'pythonemail'
	now = datetime.now()    
	datetime_subject_line = now.strftime("%m/%d/%Y @ %H:%M")
	"""
	print(path)
	with open(path, 'rb') as f:
		#img_data = f.read()
		part = MIMEApplication(f.read(), Name=str(pic_num))
		
	
	msg = MIMEMultipart()
	msg['Subject'] = 'Ding-Dong! Called 911 on ' + str(datetime_subject_line)
	#subject = 'Splash Device +------------------------------------------- Notification - ' + str(datetime_subject_line)
	msg['From'] = EMAIL_ADDRESS 
	# from_txt = EMAIL_ADDRESS
	msg['To'] = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com']
	to_txt = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com']
	# to_txt = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com', 'paucavp@wfu.edu']
	body_txt = """ """
Ding-Dong!
Look at this fool at yo door.
Image is attached.

Have a great day, bozo.
  -Frank and Andie
  
  
          
Sent on """ """+ str(datetime_subject_line)
	# email_txt = body_txt
	text = MIMEText(body_txt)
	msg.attach(text)
	
	attachment = open(path, 'rb')
	part = MIMEBase("application", "octet-stream")
	part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header("Content-Disposition", 
	"attachment; filename=%s" % str(pic_num))
	#msg.attach(part)
	
	# image = MIMEImage(img_data, name=(str(pic_num) + ".jpg"))
	# msg.attach(image)
	# part['Content-Disposition'] = 'attachment; filename="%s"' % str(pic_num)
	# msg.attach(part)
	# msg = msg.as_string()
	"""
	msg = EmailMessage()
	msg['Subject'] = 'Ding-Dong! Called 911 on ' + str(datetime_subject_line)
	msg['From'] = EMAIL_ADDRESS 
	msg['To'] = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com']
	msg.set_content("""
Ding-Dong! called 911 per your request.
Emergency services was dispatched at """ + str(now.strftime("%H:%M")) + """
Image taken at time of 911 call is attached.

Stay safe out there, and stay strapped.
  -Frank and Andie
  
  
          
Sent on """ + str(datetime_subject_line))

	with open(path, 'rb') as f:
		file_data = f.read()
		file_type = imghdr.what(f.name)
		file_name = f.name
		print(file_type, file_name)
		
		
	msg.add_attachment(file_data, maintype='image', subtype=file_type, filename="Ding-Dong! Captured Photo")

	sent = 0
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		print('started tls')
		server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		print("logged in")
		server.send_message(msg)
		server.quit()
		print("Email sent successfully")
		sent = 1
	except:
		print("Email could not be sent...")
	up_count = 0
	low_count = 0
	sent = 0
