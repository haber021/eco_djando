document.addEventListener('DOMContentLoaded', function () {
    const renderChart = (data, labels) => {
        var ctx = document.getElementById('lastChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Last Month Income',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)', // Red
                        'rgba(54, 162, 235, 0.2)', // Blue
                        'rgba(255, 206, 86, 0.2)', // Yellow
                        'rgba(75, 192, 192, 0.2)', // Green
                        'rgba(153, 102, 255, 0.2)', // Purple
                        'rgba(255, 159, 64, 0.2)' // Orange
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)', // Red
                        'rgba(54, 162, 235, 1)', // Blue
                        'rgba(255, 206, 86, 1)', // Yellow
                        'rgba(75, 192, 192, 1)', // Green
                        'rgba(153, 102, 255, 1)', // Purple
                        'rgba(255, 159, 64, 1)' // Orange
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };

    const fetchLastMonthData = () => {
        console.log("Fetching last month's income data...");
        fetch("/income/last_month_income/")
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Last month's income data:", data);
                const incomeData = data.last_month_income;
                const labels = Object.keys(incomeData);
                const values = Object.values(incomeData);
                renderChart(values, labels);
            })
            .catch(error => {
                console.error('Error fetching last month income data:', error);
            });
    };
    
    fetchLastMonthData();
});