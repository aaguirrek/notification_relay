## Notification Relay

Notification Relay Server

#### License

mit

# Push Notification Relay Server for Frappe Apps
Enable push notifications for Frappe Apps.

## Getting Started
To be able to run this application, you will need to do the following:

1. Get the app with Frappe Bench `python -m venv env`
2. Install all requirements `pip install -r requirements.txt`
4. Create a Firebase Project & get Service Account credentials [Link](https://sharma-vikashkr.medium.com/firebase-how-to-setup-a-firebase-service-account-836a70bb6646)
5. Put your Google App credentials (content of json file) in the Notification Relay Config Doctype in the Service Account field
  ``` json
{
  "type": "service_account",
  "project_id": "project-72035",
  "private_key_id": "3123jfdsj3423pqiwerew3343",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEU=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-******@app-id.iam.gserviceaccount.com",
  "client_id": "some@some.com",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xvc8f%40cxzler-72035.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
  ```
6. Follow **Register you app** under Step 1 given in the [Firebase documentation](https://firebase.google.com/docs/web/setup#register-app) and obtain the `FIREBASE_CONFIG` JSON object. Save it to `Notification Relay Config Doctype`.
7.  Follow this StackOverflow [Link](https://stackoverflow.com/a/54996207) to generate a VAPID key. Save it to `Notification Relay Config Doctype`
9.  Finally, your `Notification Relay Config Doctype` should like this
``` json
{
  "apiKey": "AIzaSyC3UVxbCkUv3l4PpyWkQZGEuwOds76sdUgk0",
  "authDomain": "xxxxxxxx-frappe.firebaseapp.com",
  "projectId": "xxxxxxxxx-frappe",
  "storageBucket": "xxxxxxxxx-frappe.appspot.com",
  "messagingSenderId": "815115xxx703",
  "appId": "1:815115xxx703:web:e89fcdadfcf8df09e4852",
  "measurementId": "G-XXXXXXXXXG"
}
```
10. Install the application in your Frappe Site
11. Add the `API_SECRET` & `API_KEY` from Administrator user or other with Role:System Admin  in ERPNext Push Notification settings and then enable the Push Notification Relay option.

