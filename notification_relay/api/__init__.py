import json
import frappe
from frappe import utils
import firebase_admin
from werkzeug.wrappers import Response
from firebase_admin import credentials



API_KEY = 'pfZOoRCW-kHtAHQcqiDvb_sy5o8Hj14J_ahUBQgPfOI'

@frappe.whitelist()
def get_config():
	config = frappe.get_doc("Notification Relay Config","Notification Relay Config")
	if isinstance(config.firebase_config,str):
		config.firebase_config = json.loads(config.firebase_config)
	if isinstance(config.service_account,str):
		config.service_account = json.loads(config.service_account)
		
	FIREBASE_CONFIG = config.firebase_config
	VAPID_PUBLIC_KEY = config.vapid_public_key
	response = Response()

	if not firebase_admin._apps: 
		cred = credentials.Certificate(config.service_account)
		firebase_admin.initialize_app(credential=cred,options=FIREBASE_CONFIG )
	res = {}
	res['vapid_public_key'] = VAPID_PUBLIC_KEY
	res['config'] = FIREBASE_CONFIG
	response = Response(json.dumps(res), content_type='application/json')
	response.status_code = 200
	return response
