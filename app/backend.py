import firebase_admin
import os
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO
from datetime import datetime
from db_manager import DatabaseManager
from mqtt_handler import MQTTManager
from flask import Flask, render_template, redirect, url_for, request, session
from firebase_admin import credentials, auth, initialize_app
from functools import wraps
import atexit

"""
    Socket and Flask
"""
app = Flask(__name__)
app.secret_key = 'ss2'
CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

"""
   DB and MQTT Handler 
"""
db_manager = DatabaseManager()
# mqtt_manager = MQTTManager(db_manager)

"""
   Creds
"""
load_dotenv()

def get_firebase_config():
    """
    Create Firebase credentials dictionary from environment variables
    """
    return {
        "type": "service_account",
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.getenv('FIREBASE_CLIENT_ID'),
        "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
        "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
        "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
    }

cred = credentials.Certificate(get_firebase_config())
firebase_admin.initialize_app(cred)


"""
    Local credentials
    save firebase_credentials.json inside the app folder, uncomment the command below and comment the code above
"""
# cred = credentials.Certificate("firebase_credentials.json"))
# firebase_admin.initialize_app(cred)

"""
   Login req
"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'uid' not in session:
            return render_template('access_denied.html')
        return f(*args, **kwargs)
    return decorated_function

"""
    Firebase config
"""
@app.route('/config', methods=['GET'])
def get_firebase_config():
    # Konfigurasi Firebase (seharusnya disimpan dalam environment variables)
    config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
    }
    return jsonify(config)


"""
   login page
"""
@app.route('/')
def index():
    return render_template('login.html')

"""
   login method
"""
@app.route('/login', methods=['POST'])
def login():
    id_token = request.form.get('idToken')
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        session['uid'] = uid
        return redirect(url_for('index')) # FOR WEB
    except Exception as e:
        print("Error verifying ID token:", e)
        return redirect(url_for('login')) # FOR WEB

"""
   Main app
"""
@app.route('/index')
@login_required
def dashboard():
    # return f"Welcome to your dashboard, User ID: {session['uid']}"
    return render_template('index.html') # FOR WEB

"""
   Logout method
"""
@app.route('/logout')
def logout():
    session.pop('uid', None)
    # return redirect(url_for('index')) FOR WEB

"""
   Historical data req
   Format : /api/fetch_data/<location>/YYYY-MM-DD%20hh:mm:ss&YYYY-MM-DD%20hh:mm:ss
"""
@app.route('/api/fetch_data/<location>/<startdate>&<enddate>', methods=['GET'])
def get_fetch_data(location, startdate, enddate):
    try:
        startdate = datetime.strptime(startdate, "%Y-%m-%d %H:%M:%S") if startdate else None
        enddate = datetime.strptime(enddate, "%Y-%m-%d %H:%M:%S") if enddate else None
        
        raw_data = db_manager.get_data(location, startdate, enddate)
        
        data = [
            {
                "id": item[0],
                "reading_time": item[1].strftime("%Y-%m-%d %H:%M:%S"),
                "position": item[2],
                "meter_type": item[3],
                "meter_serial_number": item[4],
                "active_energy_import": item[5],
                "active_energy_export": item[6],
                "reactive_energy_import": item[7],
                "reactive_energy_export": item[8],
                "apparent_energy_import": item[9],
                "apparent_energy_export": item[10]
            }
            for item in raw_data
        ]
        
        return jsonify(data)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
   Realtime data req
   Format : /api/fetch_data/<location>/last_history
"""
@app.route('/api/fetch_data/<location>/last_history', methods=['GET'])
def get_last_history(location):
    try:
        raw_data = db_manager.get_data_last_two_data(location)
        
        data = [
            {
                "id": item[0],
                "reading_time": item[1].strftime("%Y-%m-%d %H:%M:%S"),
                "position": item[2],
                "meter_type": item[3],
                "meter_serial_number": item[4],
                "active_energy_import": item[5],
                "active_energy_export": item[6],
                "reactive_energy_import": item[7],
                "reactive_energy_export": item[8],
                "apparent_energy_import": item[9],
                "apparent_energy_export": item[10]
            }
            for item in raw_data
        ]
        
        return jsonify(data)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
    Request all anomaly data
    Format : /api/fetch_data/anomaly
"""
@app.route('/api/fetch_data/anomaly', methods=['GET'])
def get_anomaly_data():
    try:
        raw_data = db_manager.get_anomaly()

        anomaly_data = [
            {
                "id": item[0],
                "position": item[1],
                "reading_time": item[2].strftime("%Y-%m-%d %H:%M:%S")
            }
            for item in raw_data
        ]
        return jsonify(anomaly_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
    Request specific anomaly data
    Format : /api/fetch_data/anomaly/<id>
"""
@app.route('/api/fetch_data/anomaly/<id>', methods=['GET'])
def get_anomaly_data_by_id(id):
    try:
        if not id.isdigit():
            return jsonify({"error": "Invalid ID format"}), 400

        raw_data = db_manager.get_anomaly_by_id(int(id))

        anomaly_data = [
            {
                "reading_time": raw_data[0].strftime("%Y-%m-%d %H:%M:%S"),
                "position": raw_data[1],
                "meter_type": raw_data[2],
                "meter_serial_number": raw_data[3],
                "active_energy_import": raw_data[4],
                "active_energy_export": raw_data[5],
                "reactive_energy_import": raw_data[6],
                "reactive_energy_export": raw_data[7],
                "apparent_energy_import": raw_data[8],
                "apparent_energy_export": raw_data[9],
                "anomaly_type": raw_data[10]
            }
        ]
        return jsonify(anomaly_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
    Main
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=False)
