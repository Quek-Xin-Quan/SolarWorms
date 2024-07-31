from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.stattools import grangercausalitytests
from darts.models import KalmanForecaster
from darts import TimeSeries
from sklearn.metrics import mean_squared_error
import math

app1 = Flask(__name__)
CORS(app1)

def detect_outliers(series, threshold=2):
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std
    return z_scores.abs() > threshold

def converting_format(data):
    data['dbtimestamp'] = pd.to_datetime(data['dbtimestamp'])
    data['dbtimestamp'] = data['dbtimestamp'].dt.round('5s')
    pivoted_data = data.pivot_table(index='dbtimestamp', columns='sensor', values='value', aggfunc='mean')
    pivoted_data_filled = pivoted_data.ffill().bfill()
    pivoted_data_filled.index = pivoted_data_filled.index + pd.Timedelta(hours=8)
    pivoted_data_filled = pivoted_data_filled.reset_index()
    pivoted_data_filled.rename(columns={
        'dbtimestamp': 'TimeFrame',
        '7 in 1 Soil Sensor Potassium': 'Potassium',
        '7 in 1 Soil Sensor Phosphorus': 'Phosphorus',
        '7 in 1 Soil Sensor Nitrogen': 'Nitrogen',
        '7 in 1 Soil Sensor PH': 'PH',
        '7 in 1 Soil Sensor EC': 'EC',
        '7 in 1 Soil Sensor Temperature': 'temperature',
        '7 in 1 Soil Sensor Moisture': 'mositure',
        'SCD41 Humidity': 'humidity',
        'SCD41 Temperature': 'SCD41 Temperature',
        'SCD41 CO2': 'CO2'
    }, inplace=True)
    pivoted_data_5min = pivoted_data_filled.set_index('TimeFrame').resample('5T').mean().reset_index()
    return pivoted_data_5min

def extract_p_values(test_results, max_lag):
    p_values = {}
    for lag in range(1, max_lag + 1):
        p_values[lag] = test_results[lag][0]['ssr_ftest'][1]    
    return p_values

def data_preprocessing():
    new_data = pd.read_csv('query.csv')
    new_data = converting_format(new_data)
    new_data = new_data[-432:]
    time_series_col = new_data.columns.to_list()

    for i in time_series_col:
        new_data[i] = new_data[i].replace(0, np.nan)
        new_data[i] = new_data[i].bfill()

    for column in new_data[time_series_col].columns:
        outliers = detect_outliers(new_data[column])
        new_data.loc[outliers, column] = np.nan
        new_data[column].fillna(new_data[column].mean(), inplace=True)

    for column in new_data.columns:
        if new_data[column].nunique() == 1:
            new_data.drop(column, axis=1, inplace=True)

    for feature in new_data.columns:
       if new_data[feature].isnull().sum() > 0:
           new_data.drop(feature, axis=1, inplace=True)

    Time_Col = new_data['TimeFrame']
    new_data.drop(['TimeFrame'], axis=1, inplace=True)

    phos_significant_features = []
    nitro_significant_features = []
    pot_significant_features = []
    max_lag = 5

    for feature in new_data.columns:
        test_result = grangercausalitytests(new_data[['Phosphorus', feature]], max_lag)
        p_values = extract_p_values(test_result, max_lag)
        if any(p_value < 0.05 for p_value in p_values.values()):
            phos_significant_features.append(feature)    
    
    for feature in new_data.columns:
        test_result = grangercausalitytests(new_data[['Nitrogen', feature]], max_lag)
        p_values = extract_p_values(test_result, max_lag)
        if any(p_value < 0.05 for p_value in p_values.values()):
            nitro_significant_features.append(feature)   

    for feature in new_data.columns:
        test_result = grangercausalitytests(new_data[['Potassium', feature]], max_lag)
        p_values = extract_p_values(test_result, max_lag)
        if any(p_value < 0.05 for p_value in p_values.values()):
            pot_significant_features.append(feature)

    final_significant_features = list(set(phos_significant_features + nitro_significant_features + pot_significant_features + ['Phosphorus', 'Nitrogen', 'Potassium']))
    new_data = new_data[final_significant_features]
    new_data['TimeFrame'] = Time_Col

    train = new_data[:int(0.8*(len(new_data)))]
    test= new_data[int(0.8*(len(new_data))):]
    train_timeframe = train['TimeFrame']
    test_timeframe = test['TimeFrame']
    train.drop('TimeFrame', axis=1, inplace=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(train)
    col_list = train.columns.to_list()
    scaled_train = pd.DataFrame(scaled_train, columns=col_list)
    scaled_train.index = train_timeframe
    scaled_train.index = scaled_train.index.to_period('10T')

    test.index = test['TimeFrame']
    test.drop('TimeFrame', axis=1, inplace=True)

    return scaled_train, test, train_timeframe, test_timeframe, scaler

def kalman_model_retraining(scaled_train, test):
    kalman_df = scaled_train.reset_index()
    kalman_df.rename(columns={'index': 'date'}, inplace=True)
    col_list = scaled_train.columns.tolist()
    series = TimeSeries.from_dataframe(kalman_df, 'TimeFrame', col_list)

    model = KalmanForecaster(dim_x=series.width)
    model.fit(series)
    return model

def model_validation(model, test, scaler):
    n_forecast = len(test)
    predict = model.predict(n_forecast)

    if isinstance(predict, TimeSeries):
        predictions = predict.pd_dataframe()
    elif isinstance(predict, (np.ndarray, list)):
        try:
            predictions = pd.DataFrame(predict, columns=test.columns)
        except ValueError as e:
            print(f"Error creating DataFrame from predictions: {e}")
            return None
    elif isinstance(predict, pd.DataFrame):
        predictions = predict
    else:
        print(f"Unexpected data type for predictions: {type(predict)}")
        return None

    if predictions.isnull().values.any():
        print("Predictions contain NaN values. Check the model and input data.")
        return None

    try:
        predictionsdf = pd.DataFrame(scaler.inverse_transform(predictions), columns=predictions.columns)
    except Exception as e:
        print(f"Error in inverse transform: {e}")
        return None

    if 'TimeFrame' in test.columns:
        forecast_validation = pd.DataFrame(predictionsdf.values, index=test['TimeFrame'], columns=predictions.columns)
    else:
        forecast_validation = pd.DataFrame(predictionsdf.values, index=test.index, columns=predictions.columns)

    return forecast_validation

def model_prediction(model, test, scaler, n_forecast=12):
    predict = model.predict(n_forecast)

    if isinstance(predict, TimeSeries):
        predictions = predict.pd_dataframe()
    elif isinstance(predict, (np.ndarray, list)):
        try:
            predictions = pd.DataFrame(predict, columns=test.columns)
        except ValueError as e:
            print(f"Error creating DataFrame from predictions: {e}")
            return None
    elif isinstance(predict, pd.DataFrame):
        predictions = predict
    else:
        print(f"Unexpected data type for predictions: {type(predict)}")
        return None

    if predictions.isnull().values.any():
        print("Predictions contain NaN values. Check the model and input data.")
        return None

    try:
        predictionsdf = pd.DataFrame(scaler.inverse_transform(predictions), columns=predictions.columns)
    except Exception as e:
        print(f"Error in inverse transform: {e}")
        return None

    start_timestamp = test.index.max() + pd.Timedelta(minutes=10)
    new_index = pd.date_range(start=start_timestamp, periods=n_forecast + 1, freq='10T')[1:]
    forecastdf = pd.DataFrame(predictionsdf.values, index=new_index, columns=predictions.columns)

    return forecastdf

def minimum_score(forecast_val, test):
    phos_valid = None
    nitro_valid = None
    potas_valid = None

    rmse_phos = math.sqrt(mean_squared_error(forecast_val['Phosphorus'], test['Phosphorus']))
    print('Mean value of Phosphorus is : {}. Root Mean Squared Error is :{}'.format(test['Phosphorus'].mean(), rmse_phos))

    rmse_nitro = math.sqrt(mean_squared_error(forecast_val['Nitrogen'], test['Nitrogen']))
    print('Mean value of Nitrogen is : {}. Root Mean Squared Error is :{}'.format(test['Nitrogen'].mean(), rmse_nitro))

    rmse_potas = math.sqrt(mean_squared_error(forecast_val['Potassium'], test['Potassium']))
    print('Mean value of Potassium is : {}. Root Mean Squared Error is :{}'.format(test['Potassium'].mean(), rmse_potas))

    min_score_dict = {'Phos_Score': 100, 'Nitro_score': 70, 'Potas_score': 200}

    if rmse_phos < min_score_dict['Phos_Score']:
        phos_valid = True
    if rmse_nitro < min_score_dict['Nitro_score']:
        nitro_valid = True
    if rmse_potas < min_score_dict['Potas_score']:
        potas_valid = True

    if phos_valid == True and nitro_valid == True and potas_valid == True:
        return True
    else:
        return False

def parse_ratio(ratio_str):
    return list(map(float, ratio_str.split(':')))

def check_ratio(row, ratio, tolerance=0.45):
    row = row / row.sum()
    ratio = np.array(ratio) / np.sum(ratio)
    return np.all(np.abs(row - ratio) <= tolerance)

def apply_ratio_check(df, ratio_str, tolerance=0.45):
    ratio = parse_ratio(ratio_str)
    return df.apply(check_ratio, axis=1, ratio=ratio, tolerance=tolerance)

@app1.route('/')
def loadpage():
    return render_template('home.html', query='')

@app1.route('/retrain', methods=['POST'])
def retrain():
    data = request.get_json()
    user_ratio = data.get('user_ratio')
    scaled_train, test, train_timeframe, test_timeframe, scaler = data_preprocessing()
    scaled_train.index = train_timeframe

    model = kalman_model_retraining(scaled_train, test)
    score_df = model_validation(model, test, scaler)
    if minimum_score(score_df, test) == True:
        forecast_df = model_prediction(model, test, scaler, n_forecast=12)
        forecast_df = forecast_df[["Nitrogen", "Phosphorus", "Potassium"]]
        forecast_df['RatioCheck'] = apply_ratio_check(forecast_df, user_ratio)
        
        print(forecast_df.head())
        forecast_html = forecast_df.to_html(classes='table table-striped')
        return jsonify({'status': 'success', 'table': forecast_html})
    else:
        return jsonify({'status': 'failure', 'message': 'Model retrained but failed the minimum score'})
    
@app1.route('/start', methods=['POST'])
def start():
    scaled_train, test, train_timeframe, test_timeframe, scaler = data_preprocessing()
    scaled_train.index = train_timeframe

    model = kalman_model_retraining(scaled_train, test)
    score_df = model_validation(model, test, scaler)
    if minimum_score(score_df, test) == True:
        user_ratio = '1:4:2'
        forecast_df = model_prediction(model, test, scaler, n_forecast=12)
        forecast_df = forecast_df[["Nitrogen", "Phosphorus", "Potassium"]]
        forecast_df['RatioCheck'] = apply_ratio_check(forecast_df, user_ratio)
        print(forecast_df.head())
        forecast_html = forecast_df.to_html(classes='table table-striped')
        return jsonify({'status': 'success', 'table': forecast_html})
    else:
        return jsonify({'status': 'failure', 'message': 'Model retrained but failed the minimum score'})

if __name__ == '__main__':
    app1.run(port=5000, debug=True)
