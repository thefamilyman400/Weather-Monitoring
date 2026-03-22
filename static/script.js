const input = document.getElementById("city");
const suggestions = document.getElementById("suggestions");
const button = document.getElementById("searchBtn");

// 🔍 Autocomplete
input.addEventListener("input", async () => {
    const query = input.value;

    if (query.length < 2) {
        suggestions.innerHTML = "";
        return;
    }

    const res = await fetch(`/autocomplete?q=${query}`);
    const data = await res.json();

    suggestions.innerHTML = "";

    data.forEach(city => {
        const div = document.createElement("div");
        div.textContent = city;

        div.onclick = () => {
            input.value = city;
            suggestions.innerHTML = "";
            loadWeather(city); // ✅ FIXED
        };

        suggestions.appendChild(div);
    });
});

// ENTER KEY SUPPORT
input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        loadWeather(input.value);
        suggestions.innerHTML = "";
    }
});

// BUTTON CLICK
button.addEventListener("click", () => loadWeather(input.value));

// AUTO LOCATION
window.onload = () => {
    navigator.geolocation.getCurrentPosition(async (pos) => {
        const res = await fetch(`/weather_by_coords?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`);
        const data = await res.json();

        updateUI(data);
        loadChart(data.city);
    });
};

function updateUI(data) {
    document.getElementById("weather-card").innerHTML = `
        <h2>📍 ${data.city}, ${data.country}</h2>
        <img src="http://openweathermap.org/img/wn/${data.icon}@2x.png">
        <p style="font-size: 28px; font-weight: bold;">${data.temp}°C</p>
        <p>${data.desc}</p>
        <hr style="border: 0.5px solid rgba(255,255,255,0.1); margin: 10px 0;">
        <p>💧 Humidity: ${data.humidity}%</p>
        <p>🌡 Pressure: ${data.pressure} hPa</p>
        <p>🕒 ${data.time}</p>
    `;
}

async function loadWeather(city) {
    if (!city) return;

    try {
        const res = await fetch(`/weather_by_city?city=${city}`);
        const data = await res.json();

        if (data.error) {
            alert("City not found");
            return;
        }

        updateUI(data);
        loadChart(city);
    } catch (err) {
        console.error(err);
        alert("Error fetching weather");
    }
}

async function loadChart(city) {
    const res = await fetch(`/forecast?city=${city}`);
    const data = await res.json();

    const ctx = document.getElementById("weatherChart").getContext("2d");

    if (window.chart) window.chart.destroy();

    const labels = data.times.map(t => {
        const d = new Date(t);
        return d.toLocaleDateString("en-US", { weekday: "short" });
    });

    // 🌈 Gradient Glow
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, "rgba(56,189,248,0.4)");
    gradient.addColorStop(1, "rgba(56,189,248,0)");

    window.chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                data: data.temps,
                borderColor: "#38bdf8",
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 5,
                pointBackgroundColor: "#38bdf8",
                pointBorderWidth: 2
            }]
        },
        options: {
            animation: {
                duration: 1200,
                easing: "easeOutQuart"
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: "#020617",
                    titleColor: "#fff",
                    bodyColor: "#38bdf8",
                    borderColor: "#38bdf8",
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `Temp: ${context.raw}°C`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#94a3b8"
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    ticks: {
                        color: "#94a3b8"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.05)"
                    }
                }
            }
        }
    });
}