# Monitoring Dashboard

## Description
In this project, many of the variables such as MQTT topics, MQTT brokers, and data metrics are currently set as dummy values. These are placeholder values used during development to simulate the functionality of the system. They allow the system to run in a controlled environment without requiring actual IoT devices or data sources to be connected.

## Repository
Make sure to use this command before commit and push changes to the remote repository to prevent this **warning: LF will be replaced by CRLF.**
```
git config --global core.autocrlf false
```

## API Documentation
### GET /config
Description: Retrieves Firebase configuration required for the frontend application.

| Parameter  | Type | Description |
| ------------- |:-------------:|:-------------:|
| None     | N/A     | 	Retrieves Firebase configuration such as API Key, Project ID, and other necessary details. |

Response
```
{
    "apiKey": "your-api-key",
    "authDomain": "your-auth-domain",
    "projectId": "your-project-id",
    "storageBucket": "your-storage-bucket",
    "messagingSenderId": "your-messaging-sender-id",
    "appId": "your-app-id",
    "measurementId": "your-measurement-id"
}
```

### POST /login
Description: Logs the user in using a Firebase ID token.

| Parameter  | Type | Description |
| ------------- |:-------------:|:-------------:|
| idToken     | string     | 	Firebase ID token obtained after a successful login using Firebase Authentication.     |

Response :
```
200 OK: Redirects to the main page (/index) if login is successful.
301 Moved Permanently: Redirects back to the login page if login fails.
```

### GET /index
Description: Displays the dashboard page after successful login.

| Parameter  | Type | Description |
| ------------- |:-------------:|:-------------:|
| None     | N/A     | 	Accesses the dashboard page after a successful login.     |

Response :
```
200 OK: Returns the HTML page of the user's dashboard.
```

### GET /logout
Description: Logs the user out and clears the session.

| Parameter  | Type | Description |
| ------------- |:-------------:|:-------------:|
| None     | N/A     | 	Clears the user session and redirects to the login page.     |

Response :
```
200 OK: User is redirected back to the login page.
```

### GET /api/fetch_data
Description: Retrieves historical data based on the specified time range (startdate and enddate).

| Parameter  | Type | Description |
| ------------- |:-------------:|:-------------:|
| startdate     | string     | 	Start time in `YYYY-MM-DD%20HH:MM:SS` format.     |
| enddate     | string     | 	End time in `YYYY-MM-DD%20HH:MM:SS` format.     |

Example:
```
http://34.31.231.164:5000/api/fetch_data?startdate=2024-11-01%2000:12:23&endddate=2024-11-18%2000:15:23
```

Response:
```
[
  {
    "active_energy_export": 0,
    "active_energy_import": 19638,
    "apparent_energy_export": 0,
    "apparent_energy_import": -4386111,
    "id": 1,
    "meter_serial_number": 56580,
    "meter_type": "mk10m",
    "position": "A",
    "reactive_energy_export": 0,
    "reactive_energy_import": 2938,
    "reading_time": "2024-11-16 20:44:28"
  },
  {
    "active_energy_export": 0,
    "active_energy_import": -46010,
    "apparent_energy_export": 0,
    "apparent_energy_import": -4083345,
    "id": 2,
    "meter_serial_number": 69632,
    "meter_type": "mk10m",
    "position": "B",
    "reactive_energy_export": 0,
    "reactive_energy_import": -517,
    "reading_time": "2024-11-16 20:44:31"
  },
  {
    .....
  }
}
```

## MQTT Documentation
Broker (Host) : `34.42.59.154`

Port : `8080`

Topic (Dummy) : `evomo\final_data\loc_a, evomo\final_data\loc_a, evomo\final_data\loc_b`

Example of implementation is on app/static/js/script.js

## GCP Deployment
Protocol : `http`

url : `34.31.231.164`

post : `5000`

## Credentials
Save .env in root directory
```
# Firebase Admin SDK credentials
FIREBASE_PROJECT_ID=auth-login-f60fe
FIREBASE_PRIVATE_KEY_ID=792fd205d960cfac76e637dfb28e6b73930b8d7c
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxdhWXwSnSpICP\nSXhEz/ZQ/xvpzg3TE6Cxn+g71t0GP2n0lzEzeWOTwqFbkKSaSs8Lyd+GibfEzexA\n4LtYn+t2ZCz6Jagz6EPp/U07fd7ulZql1ZCAKw25cZkWaJg1S37zuJXsSttBcQlF\njhMPcGjyUKvfqKFjdPAeOZo4nC79oeNi/gVWphZs+0KHG/zVsJCQuUCZWbgyMD+d\nRZLXsetgYj9xTvpGug6E7j0uacI0pPHZKSHR9jUBVrfoLiuWTZhWJAlwQGK2LhXv\nEWeoQl+9sLyeGrM7YWYpFsGUv2WtTewUYnI66XQa1t8Y1RsRApuRT+mDFScKhdjL\nSHU1CFJ7AgMBAAECggEAA11MQoDIhLRWtaC8dX2F23pCsreT3oUYPlXcRsonjZdF\nMHxvU90AzMvbWEuRO1WgwEX3BWt1/vayfHZmRuNdSPTUP3fYTQehxf1l6fNUdyyB\n7pPydeObEoF7WAfqntQMF53PxdeTeZWlidqMNPY6HyH1aDuft61/YetQp7MaVvej\nKeckoLIcghSBx8sduSfuCE/YVbRG+Pbr75MeHbd8Kr+bf57P+1tr14CHJEGq70Gh\nhz3LmloeXGeVLzDR3wxcGGXcEGqXpCSOlZ1LYVGmOGXOzVxHNojMG1gGneSlBG2Y\nEEzyWKmsRLw4H3NqUjs2uPTYeKfe93DJkOjpjVYRAQKBgQDiFb1yrETf4U0CGMSK\nTBquQonObT1vrmOIjxkOv5dY5zoyB8HXW+aTOkcwPOCR6lnNs7dbakaeW4TlWHif\n9V7Rys1uNF0qFaDih+2xRGb0g7iOpB/UQk/pxVcOFH5B0qtzRZ6OY9egJtvIEC7L\nblZ0C7eY2n4HiK1w3hcJOo4HewKBgQDI8UwAabz1z5EF9TavKLeIN8Cr2jAhHLNK\nRN2Ql+2uIxRtlZQ5PL7WRbwJYd1rBrM73eIYygXFT2Ymdvvk3pfMd1yxORLoHx63\n865gPlo53v+oounBPUOgaroLFUSO3/f6h3l7DFN28lXGcEcrV8VnQUeqsjQY8+/k\nia6YvXdxAQKBgQDg7B/95cTftpWWcG2X6P7iPvA6nhNw+F2tji+vrIw1tlT/URhX\n2OYbsu7/3pDMmgmdzB2upJx9Dy+3u7zF5qbesJSP/yhwpfPZasHeid6jhCgoQMAp\nu48lU164c0ro0V4g4DJOFqZ+fipJb1AeszbvXHjbaQPZGvDySQFB/S8v4QKBgAlA\n42kZdXQ0bM9DbZM/YsRJHPxM/e5obfE7nqBr/qwIPYaWXs8L9xXS/EfKU/H7ywE0\nxJazpvRhJakbzZnKjl8CGCipIi/CTx3VgPA5rtn/ZPKVHgKiGZ0njQ25mwChW8AT\nwQpjlOxjWIPc48ohLpwEq5I2xqNniGKT3JB4GSoBAoGBAMtxY6kDrhzOxjA3sQqE\nTcIMFnru5UytrO8Usy5ETeUoOewlumBzH7FUVkAi/q3zOPQfjimnqNyaBzqTrIeT\n9jHU+xpjRBK7dFpmad89N80dNgoCHDLK8mIImqZF5Nx2bD1PuJZcmt4XGTIDcdzi\nuf1siSRlFDh4w8lqi4RgYe6i\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-22xwl@auth-login-f60fe.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=114365098387079737180
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-22xwl%40auth-login-f60fe.iam.gserviceaccount.com
FIREBASE_UNIVERSE_DOMAIN=googleapis.com

# Firebase Client SDK config
FIREBASE_API_KEY=AIzaSyDV9FCj2T3icEA-_iqY6cFV9K1Xzyg2BbQ
FIREBASE_AUTH_DOMAIN=auth-login-f60fe.firebaseapp.com
FIREBASE_STORAGE_BUCKET=auth-login-f60fe.appspot.com
FIREBASE_MESSAGING_SENDER_ID=366471157245
FIREBASE_APP_ID=1:366471157245:web:d81f538667dc78ac3fb594
FIREBASE_MEASUREMENT_ID=G-2FE7RTW0X6
```

## To-Do List

### 1. **Implement Gunicorn for Production Deployment**
~~- Gunicorn will handle multiple concurrent requests, ensuring better performance and scalability than the built-in Flask development server.~~
~~- The application will be set up to run with Gunicorn in the production environment.~~

### 2. **Implement Supervisor for Process Management**
~~- Supervisor will be used to ensure that Gunicorn is always running.~~
~~- If the Gunicorn process crashes or fails, Supervisor will automatically restart it. This is crucial for maintaining the stability of the system in a production environment.~~

### 3. **Implement ML API Endpoints for Anomaly Detection**
- The machine learning models will be stored in cloud storage (Google Cloud Storage) for easy access and version control.
- The endpoints will interact with the machine learning models to provide real-time anomaly detection for the system.

### 4. **Fix Dockerfile**
- The Dockerfile should be reviewed and updated

### 5. **Integrate with Evomo Real Data**
- The system will be connected to the Evomo platform’s MQTT broker, subscribing to real data topics (e.g., energy readings from IoT devices).
- The real-time data will be processed by the backend (including anomaly detection) and stored for analysis.
- The dashboard will display real-time data and anomalies, making the monitoring system fully operational with live inputs from Evomo.

### 6. **Implement Firebase Cloud Messaging (FCM) for Anomaly Notifications**
- Set up Firebase in the backend to send notifications to mobile devices via FCM. This involves configuring Firebase credentials and initializing Firebase in the Flask app.
