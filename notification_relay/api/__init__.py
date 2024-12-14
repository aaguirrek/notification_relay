import json
import frappe
from frappe import utils
import firebase_admin
from werkzeug.wrappers import Response


API_KEY = 'pfZOoRCW-kHtAHQcqiDvb_sy5o8Hj14J_ahUBQgPfOI'

@frappe.whitelist()
def get_config():
	config = frappe.get_doc("Notification Relay Config","Notification Relay Config")
	if isinstance(config.firebase_config,str):
		config.firebase_config = json.loads(config.firebase_config)
	FIREBASE_CONFIG = config.firebase_config
	VAPID_PUBLIC_KEY = config.vapid_public_key
	response = Response()
	if not firebase_admin._apps: 
		firebase_admin.initialize_app(options=FIREBASE_CONFIG)
	res = {}
	res['vapid_public_key'] = VAPID_PUBLIC_KEY
	res['config'] = FIREBASE_CONFIG
	response = Response(json.dumps(res), content_type='application/json')
	response.status_code = 200
	return response

@frappe.whitelist()
def getfavicon():
	return json.loads(frappe.get_doc("Notification Relay Config","Notification Relay Config").firebase_config)["apiKey"]
	return utils.get_url(frappe.get_website_settings("favicon"),True)