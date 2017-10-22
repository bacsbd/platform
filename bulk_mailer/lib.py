import requests

DOMAIN_NAME = 'no-reply.bacsbd.org'
API_KEY = 'PUT-YOUR-KEY'
SENDER_NAME = 'Bangladesh Advanced Computing Society <no-reply@bacsbd.org>'

def send_html_message(email, subject, body, html=False):
	data = {
		'from': SENDER_NAME,
		'to': email,
		'subject': subject
	}

	if html:
		data['html'] = body
	else:
		data['text'] = body

	return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % DOMAIN_NAME,
        auth=("api", API_KEY),
        data=data)