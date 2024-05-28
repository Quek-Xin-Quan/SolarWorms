
const compost_dashboard = document.getElementById('compost-dashboard');
const solar_dashboard = document.getElementById('solar-dashboard');
const anomaly_detection1 = document.getElementById('anomaly-detection1');
const anomaly_detection2 = document.getElementById('anomaly-detection2');
const heat = document.getElementById('heat');
const humidity = document.getElementById('humidity');
const temperature = document.getElementById('temperature');
const light = document.getElementById('light');
const nitrogen = document.getElementById('nitrogen');
const phosphorus = document.getElementById('phosphorus');
const potassium = document.getElementById('potassium');
const prediction = document.getElementById('prediction');
const sensor = document.getElementById('sensor');
const forecast = document.getElementById('forecast');




const compost_dashboard_div = document.getElementById('compost-dashboard-div');
const solar_dashboard_div = document.getElementById('solar-dashboard-div');
const power_anomaly_detection_01 = document.getElementById('power_anomaly_detection_01');
const power_anomaly_detection_02 = document.getElementById('power_anomaly_detection_02');
const heat_outlier = document.getElementById('heat-outlier');
const humidity_outlier = document.getElementById('humidity-outlier');
const temperature_outlier = document.getElementById('temperature-outlier');
const light_outlier = document.getElementById('light-outlier');
const nitrogen_outlier = document.getElementById('nitrogen-outlier');
const phosphorus_outlier = document.getElementById('phosphorus-outlier');
const potassium_outlier = document.getElementById('potassium-outlier');
const energy_prediction = document.getElementById('energy-prediction');
const sensor_div = document.getElementById('sensor-overview-div');
const npk_forecast = document.getElementById('npk-forecast');


forecast.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "block";


});


sensor.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "block";
    npk_forecast.style.display = "none";

});

prediction.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "block";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});



heat.addEventListener('click', () => {
    heat_outlier.style.display = "block";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});
humidity.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "block";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});
temperature.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "block";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});
light.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "block";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});
nitrogen.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "block";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});
phosphorus.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "block";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";


});
potassium.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "block";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";

});




compost_dashboard.addEventListener('click', () => {
    
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "block";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";

    
});

solar_dashboard.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "block";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";

});

anomaly_detection1.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "block";
    power_anomaly_detection_02.style.display = "none";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";

    
});

anomaly_detection2.addEventListener('click', () => {
    heat_outlier.style.display = "none";
    humidity_outlier.style.display = "none";
    temperature_outlier.style.display = "none";
    light_outlier.style.display = "none";
    nitrogen_outlier.style.display = "none";
    phosphorus_outlier.style.display = "none";
    potassium_outlier.style.display = "none";
    compost_dashboard_div.style.display = "none";
    solar_dashboard_div.style.display = "none";
    power_anomaly_detection_01.style.display = "none";
    power_anomaly_detection_02.style.display = "block";
    energy_prediction.style.display = "none";
    sensor_div.style.display = "none";
    npk_forecast.style.display = "none";

});




document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.dropdown');
    dropdown.addEventListener('mouseenter', () => {
      dropdown.querySelector('.submenu').style.display = 'block';
    });
  
    dropdown.addEventListener('mouseleave', () => {
      dropdown.querySelector('.submenu').style.display = 'none';
    });
});