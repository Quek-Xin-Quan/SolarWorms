const compost_dashboard = document.getElementById('compost-dashboard');
const solar_dashboard = document.getElementById('solar-dashboard');

const compost_dashboard_div = document.getElementById('compost-dashboard-div');
const solar_dashboard_div = document.getElementById('solar-dashboard-div');


compost_dashboard.addEventListener('click', () => {
    
    compost_dashboard_div.style.display = "block";
    solar_dashboard_div.style.display = "none";
    
});

solar_dashboard.addEventListener('click', () => {
    solar_dashboard_div.style.display = "block";
    compost_dashboard_div.style.display = "none";
    

});