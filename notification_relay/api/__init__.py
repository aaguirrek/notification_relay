import json
import frappe
import firebase_admin
from werkzeug.wrappers import Response
from firebase_admin import credentials


@frappe.whitelist()
def get_config():
	config = frappe.get_doc("Notification Relay Config","Notification Relay Config")
	if isinstance(config.firebase_config,str):
		config.firebase_config = json.loads(config.firebase_config)
	if isinstance(config.service_account,str):
		config.service_account = json.loads(config.service_account)
	response = Response()
	if not firebase_admin._apps: 
		cred = credentials.Certificate(config.service_account)
		firebase_admin.initialize_app(credential=cred,options=config.firebase_config )
	res = {}
	res['vapid_public_key'] = config.vapid_public_key
	res['config'] = config.firebase_config
	response = Response(json.dumps(res), content_type='application/json')
	response.status_code = 200
	return response
