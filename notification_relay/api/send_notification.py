import json

import firebase_admin
import frappe
from frappe import utils
from firebase_admin import messaging
import frappe.hooks
from .my_secrets import FIREBASE_CONFIG

@frappe.whitelist()
def user():
	
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	title = frappe.request.args.get('title')
	body = frappe.request.args.get('body')
	data = json.loads(frappe.request.args.get('data'))
	
	if not firebase_admin._apps: 
		firebase_admin.initialize_app(options=FIREBASE_CONFIG)
	if isinstance(data,str):
		data = json.loads(data)
	registration_tokens = []
	
	if frappe.db.exists("relay_user_device_map",f"{key}-{user_id}") != None:
		doc = frappe.get_doc("relay_user_device_map",f"{key}-{user_id}")
		registration_tokens=[]
		for i in doc.devices:
			registration_tokens.append(i.key)
		message = messaging.MulticastMessage(
			webpush=messaging.WebpushConfig(
				notification=messaging.WebpushNotification(
					title=title,
					body=body,
					icon=utils.get_url(frappe.get_website_settings("favicon"),True),
				),
				fcm_options=messaging.WebpushFCMOptions(link=data.get('click_action')),
			),
			tokens=registration_tokens
		)
		response = messaging.send_multicast(message)
		print('Successfully sent message:', response)
		
		response = {
				'success':200,
				'message':f'Notiifcation sent to {user_id} user'
		}
		return response
	return 'User registration not found', 400


@frappe.whitelist()
def topic():
	
	topic = frappe.request.args.get('topic')
	title = frappe.request.args.get('title')
	body = frappe.request.args.get('body')
	data = json.loads(frappe.request.args.get('data'))
	if not firebase_admin._apps: 
		firebase_admin.initialize_app(options=FIREBASE_CONFIG)
	if isinstance(data,str): 
		data = json.loads(data)
	message = messaging.Message(
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title=title,
                body=body,
                icon=utils.get_url(frappe.get_website_settings("favicon"),True),
            ),
			fcm_options=messaging.WebpushFCMOptions(link=data.get('click_action')),
        ),
        topic=topic,
    )
	response = messaging.send(message)
	print('Successfully sent message:', response)
	response = {
			'success':200,
			'message':f'Notiifcation sent to {topic} topic'
	}
	return response