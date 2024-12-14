import frappe
import json
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials


@frappe.whitelist()
def subscribe():
	
	config = frappe.get_doc("Notification Relay Config","Notification Relay Config")
	if isinstance(config.firebase_config,str):
		config.firebase_config = json.loads(config.firebase_config)
		
	if isinstance(config.service_account,str):
		config.service_account = json.loads(config.service_account)

	FIREBASE_CONFIG = config.firebase_config
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	topic_name = frappe.request.args.get('topic_name')

	if not firebase_admin._apps: 
		cred = credentials.Certificate(config.service_account)
		firebase_admin.initialize_app(credential=cred,options=FIREBASE_CONFIG )

	if frappe.db.exists("relay_user_device_map",f"{key}-{user_id}") != None:
		doc = frappe.get_doc("relay_user_device_map",f"{key}-{user_id}")
		registration_tokens=[]
		for i in doc.devices:
			registration_tokens.append(i.key)
		response = messaging.subscribe_to_topic(registration_tokens, topic_name)
		print(response.success_count, 'tokens were subscribed successfully')
		response = {
			'success':200,
			'message':'User subscribed'
			}
		return response
	return "User token not registered", 400

@frappe.whitelist()
def unsubscribe():
	
	config = frappe.get_doc("Notification Relay Config","Notification Relay Config")
	if isinstance(config.firebase_config,str):
		config.firebase_config = json.loads(config.firebase_config)
		
	if isinstance(config.service_account,str):
		config.service_account = json.loads(config.service_account)

	FIREBASE_CONFIG = config.firebase_config
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	topic_name = frappe.request.args.get('topic_name')
	

	if not firebase_admin._apps: 
		cred = credentials.Certificate(config.service_account)
		firebase_admin.initialize_app(credential=cred,options=FIREBASE_CONFIG )

	if frappe.db.exists("relay_user_device_map",f"{key}-{user_id}") != None:
		doc = frappe.get_doc("relay_user_device_map",f"{key}-{user_id}")
		registration_tokens=[]
		for i in doc.devices:
			registration_tokens.append(i.key)

		response = messaging.unsubscribe_from_topic(registration_tokens, topic_name)
		print(response.success_count, 'tokens were unsubscribed successfully')
		response = {
			'success':200,
			'message':'User unsubscriber'	
		}
		return response
	return "User token not registered", 400
