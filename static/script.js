const input = document.getElementById("city");
const suggestions = document.getElementById("suggestions");
const form = document.getElementById("searchForm");

// SEARCH (NO RELOAD)
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const city = input.value;

    const res = await fetch(`/weather_by_city?city=${city}`);
    const data = await res.json();

    updateUI(data);
    loadChart(city);
});

// AUTO LOCATION
window.onload = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;

            const res = await fetch(`/weather_by_coords?lat=${lat}&lon=${lon}`);
            const data = await res.json();

            updateUI(data);
            loadChart(data.city);
        });
    }
};

// UPDATE WEATHER UI
function updateUI(data) {
    const card = document.getElementById("weather-card");

    card.innerHTML = `
        <h2>${data.city}, ${data.country}</h2>
        <p style="font-size:28px">${data.temp}°C</p>
        <p>${data.desc}</p>

        <div class="grid">
            <p>Humidity: ${data.humidity}%</p>
            <p>Pressure: ${data.pressure}</p>
            <p>Wind: ${data.wind_speed} m/s</p>
            <p>Clouds: ${data.clouds}%</p>
        </div>

        <p style="margin-top:10px">${data.time}</p>
    `;
}

// CHART
async function loadChart(city) {
    const res = await fetch(`/forecast?city=${city}`);
    const data = await res.json();

    const ctx = document.getElementById("weatherChart").getContext("2d");

    if (window.chart) {
        window.chart.destroy();
    }

    window.chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.times.map(t => t.split(" ")[0]),
            datasets: [{
                label: "Temp (°C)",
                data: data.temps,
                borderColor: "#38bdf8",
                borderWidth: 2,
                tension: 0.4
            }]
        }
    });
}