from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("RegistrationData").sheet1

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        # Prepare data for Google Sheets
        row_data = [
            data['name'],
            data['phone'],
            data['uid'],
            data['address'],
            data['serviceCategory'],
            data['subCategory'],
            data['registrationType'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        # Append to Google Sheet
        sheet.append_row(row_data)
        
        return jsonify({"success": True, "message": "Registration successful"})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/get_registrations')
def get_registrations():
    try:
        records = sheet.get_all_records()
        return jsonify({"success": True, "data": records})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)