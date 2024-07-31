import os
import urllib.request
import sys
import json
import pandas as pd
import warnings
from sqlalchemy import create_engine
from flask import Flask, request, redirect, url_for, flash, jsonify, render_template

# Ignore all warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 25)

app2 = Flask(__name__)
app2.config['UPLOAD_FOLDER'] = 'uploads'
app2.secret_key = 'your_secret_key'

def pre_merge_stage(dpm_file, inv_file):
    data_dpm = pd.read_excel(dpm_file)
    data_inv = pd.read_excel(inv_file)

    # Merging the dataframes
    merged_data = pd.merge(data_dpm, data_inv, on=['Date and Time', 'Location Code'], suffixes=('_dpm', '_inv'))

    return merged_data

def merged_preprocess(dpm_file, inv_file):
    merged_data = pre_merge_stage(dpm_file, inv_file)

    columns = ['Date and Time', 'PanelCode','BlockNo','Energy kWh_dpm', 'Expected Value kWh','Energy kWh_inv','IRR Value W/m²', 'PR %','DPMSensorIssue','INVSensorIssue']
    merged_data['BlockNo'] = merged_data['Location Code'].str.extract(r'(\d{2})')
    merged_data['SensorNo'] = merged_data['Sensor ID'].str.extract(r'(\d{2})$')
    merged_data['PanelCode'] = merged_data['BlockNo'] + '-' + merged_data['SensorNo']
    merged_data['INVSensorIssue'] = merged_data.apply(lambda row: 'Issue' if row['Energy kWh_dpm'] > row['Energy kWh_inv'] else 'No Issue', axis=1)
    sorted_data = merged_data.sort_values(by=['Date and Time', 'SensorNo'])

    cleaned_merged = sorted_data[columns]
    cleaned_merged = cleaned_merged.rename(columns={'Date and Time': 'RecordDate', 'Energy kWh_dpm': 'DPM','Expected Value kWh': 'ExpectedDPM', 'Energy kWh_inv': 'INV','IRR Value W/m²': 'IRR','PR %': 'PR',})

    return cleaned_merged

def api_date_retrieval(file_path):
    data = pd.read_excel(file_path)
    data_date_amend = data.copy()
    data_date_amend['Date and Time'] = pd.to_datetime(data_date_amend['Date and Time'])

    earliest_date = data_date_amend['Date and Time'].min().date().strftime('%Y-%m-%d')
    latest_date = data_date_amend['Date and Time'].max().date().strftime('%Y-%m-%d')

    return earliest_date, latest_date

def api_data_retrieval(file_path):

    earliest_date, latest_date = api_date_retrieval(file_path)
  
    try: 
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Clementi,Singapore/{earliest_date}/{latest_date}?unitGroup=us&key=MAEVMCSQZL8TPWXXYV5FQSLBJ&contentType=json"
        ResultBytes = urllib.request.urlopen(url)

        jsonData = json.load(ResultBytes)
          
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()

    return jsonData

def api_data_preprocessing(file_path):

    some_data = api_data_retrieval(file_path)

    columns_to_extract = ['datetime', 'conditions', 'temp', 'tempmax', 'tempmin', 'precip','cloudcover','solarenergy',
                        'solarradiation', 'windspeed', 'uvindex', 'humidity', 'dew', 'pressure', 'visibility']

    weather_data = some_data['days'] if 'days' in some_data else some_data

    # Convert the list of dictionaries to a DataFrame
    df = pd.json_normalize(weather_data)
    extracted_df = df[columns_to_extract]
    extracted_df['temp'] = (extracted_df['temp'] - 32) * (5/9)
    extracted_df = extracted_df.round(2)
    extracted_df['uvindex'] = extracted_df['uvindex'].astype(int)
    extracted_df = extracted_df.rename(columns={'datetime': 'RecordDate', 'conditions': 'Conditions','temp': 'Temp', 'tempmax': 'TempMax','tempmin': 'TempMin', 'precip': 'Precipitation',
                                                'cloudcover': 'CloudCover', 'solarenergy': 'SolarEnergy','solarradiation': 'SolarRadiation', 'windspeed': 'WindSpeed','uvindex': 'UVIndex',
                                                'humidity': 'Humidity','dew': 'Dew', 'pressure': 'Pressure','visibility': 'Visibility'})

    return extracted_df

def preprocess_data(dpm_file, inv_file):
    
    main_data = merged_preprocess(dpm_file, inv_file)
    weather_data = api_data_preprocessing(dpm_file)
    final_data = pd.merge(main_data, weather_data, on=['RecordDate'])

    return final_data

@app2.route('/')
def upload_files():
    return render_template('upload.html')

@app2.route('/process', methods=['POST'])
def process_files():
    if 'dpm_file' not in request.files or 'inv_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    dpm_file = request.files['dpm_file']
    inv_file = request.files['inv_file']
    if dpm_file.filename == '' or inv_file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if dpm_file and inv_file:
        dpm_file_path = os.path.join(app2.config['UPLOAD_FOLDER'], dpm_file.filename)
        inv_file_path = os.path.join(app2.config['UPLOAD_FOLDER'], inv_file.filename)
        dpm_file.save(dpm_file_path)
        inv_file.save(inv_file_path)

        # Process the uploaded files
        final_data = preprocess_data(dpm_file_path, inv_file_path)

        # Connect to Azure SQL Database and write the DataFrame
        server = 'dscpserver.database.windows.net'
        database = 'DSCPDatabase'
        username = 'admindscp'
        password = 'T01b26121gH'
        driver = 'ODBC Driver 17 for SQL Server'
        connection_timeout = 30  # Set your desired timeout in seconds

        conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};Connection Timeout={connection_timeout};'
        engine = create_engine(f'mssql+pyodbc:///?odbc_connect={conn_str}')

        table_name = 'newTable'
        final_data.to_sql(table_name, con=engine, index=False, if_exists='append')

        processed_json = final_data.to_json(orient='split')
        return jsonify({'data': processed_json})
        

if __name__ == '__main__':
    if not os.path.exists(app2.config['UPLOAD_FOLDER']):
        os.makedirs(app2.config['UPLOAD_FOLDER'])
    app2.run(port=5001, debug=True)
