from jinja2 import Template
from bulk_mailer.lib import send_html_message
import sys
import csv


DEBUG = False

with open('templates/contest_invitation.html', encoding='utf-8') as fp:
	html = fp.read()

with open("users.csv", encoding="utf-8") as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		data = {
			'link': "https://toph.co/c/bacs-camp-2017-s",
			'fullname': row['FullName'].encode('ascii', 'ignore').decode('ascii'),
			'handle': row['Handle'].encode('ascii', 'ignore').decode('ascii'),
			'password': row['Password'].encode('ascii', 'ignore').decode('ascii'),
		}

		email = row['Email'].encode('ascii', 'ignore').decode('ascii')

		print(data, email)

		bodyTemplate = Template(html).render(**data)

		if not DEBUG:
			send_html_message(email, 'ID and Rules of Online Selection Contest', bodyTemplate, True)
			print("mail sent to %s" % email)
