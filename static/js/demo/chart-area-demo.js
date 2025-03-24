// Set new default font family and font color to mimic Bootstrap's default styling
// Chart Defaults
// Ensure Chart.js is loading
// Ensure Chart.js is loading
console.log("Chart.js loaded");

// Function to format numbers
function number_format(number) {
    return new Intl.NumberFormat().format(number);
}

// Fetch Data from Django API
fetch('/api/weekly-sales-data/')
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Data:", data); // Debugging

        var ctx = document.getElementById("myCreativeChart").getContext("2d");

        // Create gradient effect
        var gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, "rgba(78, 115, 223, 0.3)"); // Light blue
        gradient.addColorStop(1, "rgba(78, 115, 223, 0)"); // Transparent fade

        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,  // Days of the week
                datasets: [{
                    label: "Weekly Sales",
                    data: data.earnings,
                    borderColor: "#4e73df", // Primary blue
                    backgroundColor: gradient, // Gradient fill
                    pointRadius: 6,
                    pointBackgroundColor: "#4e73df",
                    pointBorderColor: "#fff",
                    pointHoverRadius: 10,
                    borderWidth: 3,
                    tension: 0.4, // Smooth curve effect
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                        labels: {
                            color: "#333",
                            font: { size: 14, family: "Poppins, sans-serif" }
                        }
                    },
                    tooltip: {
                        enabled: true,
                        backgroundColor: "rgba(0,0,0,0.8)",
                        titleFont: { size: 14, weight: "bold" },
                        bodyFont: { size: 13 },
                        cornerRadius: 8,
                        callbacks: {
                            label: function(tooltipItem) {
                                return "Ksh " + number_format(tooltipItem.raw);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: "#4e73df",
                            font: { size: 14, family: "Poppins, sans-serif" }
                        },
                        grid: { display: false }
                    },
                    y: {
                        ticks: {
                            callback: function(value) {
                                return "Ksh " + number_format(value);
                            },
                            color: "#4e73df",
                            font: { size: 14, family: "Poppins, sans-serif" }
                        },
                        grid: {
                            borderDash: [5],
                            color: "rgba(0,0,0,0.1)"
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error loading chart data:', error));
