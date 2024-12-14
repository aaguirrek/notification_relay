import json
import frappe
from frappe import utils
import firebase_admin
from werkzeug.wrappers import Response


from .my_secrets import  FIREBASE_CONFIG, VAPID_PUBLIC_KEY
API_KEY = 'pfZOoRCW-kHtAHQcqiDvb_sy5o8Hj14J_ahUBQgPfOI'

@frappe.whitelist()
def get_config():
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
	
	return utils.get_url(frappe.get_website_settings("favicon"),True)