import frappe

@frappe.whitelist()
def add():
	
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	fcm_token = frappe.request.args.get('fcm_token')
	key = f'{project_name}_{site_name}'
	if frappe.db.exists("relay_user_device_map",f"{key}-{user_id}") != None:
		doc = frappe.get_doc("relay_user_device_map",f"{key}-{user_id}")
		doc.devices.append(frappe.get_doc({
			"doctype":"map_user_table",
			"key":fcm_token
		}))
		doc.save()
	else:
		doc = frappe.get_doc({
			"doctype":"relay_user_device_map",
			"key":key,
			"user_id":user_id,
			"devices":[frappe.get_doc({
						"doctype":"map_user_table",
						"key":fcm_token
					})]
			})
		doc.insert()
	response = {
			'success':200,
			'message':'User Token added'
	}
	return response


@frappe.whitelist()
def remove():
	project_name = frappe.request.args.get('project_name')
	site_name = frappe.request.args.get('site_name')
	key = f'{project_name}_{site_name}'
	user_id = frappe.request.args.get('user_id')
	fcm_token = frappe.request.args.get('fcm_token')


	if frappe.db.exists("relay_user_device_map",f"{key}-{user_id}") != None:
		doc = frappe.get_doc("relay_user_device_map",f"{key}-{user_id}")
		devices = []
		for device in doc.devices:
			if fcm_token != device.key:
				devices.append(device)
		doc.save()
	response = {
			'success':200,
			'message':'User Token removed'
	}
	return response