import frappe
from firebase_admin import messaging
import firebase_admin
from .my_secrets import FIREBASE_CONFIG


@frappe.whitelist()
def subscribe():
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	topic_name = frappe.request.args.get('topic_name')

	if not firebase_admin._apps: 
		firebase_admin.initialize_app(options=FIREBASE_CONFIG)
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
	
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	topic_name = frappe.request.args.get('topic_name')
	
	if not firebase_admin._apps: 
		firebase_admin.initialize_app(options=FIREBASE_CONFIG)
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
