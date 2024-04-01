document.addEventListener('DOMContentLoaded', function () {
    const renderChart = (data, labels) => {
        var ctx = document.getElementById('Mychart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: "Todays Sales",
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
                plugins: {
                    title: {
                        display: true,
                        text: 'To days sales'
                    }
                }
            }
        });
    }


    const getLineChartData = () => {
        console.log("fetching line chart data");
        fetch("/income/income_trend_over_time/")
            .then((res) => res.json())
            .then((results) => {
                console.log("line chart results", results);
                const trend_data = results.income_trend_data;
    
                if (trend_data && trend_data.today) {
                    const todaySales = trend_data.today;
                    const labels = Object.keys(todaySales);
                    const data = Object.values(todaySales);
    
                    renderChart(data, labels);
                } else {
                    console.error("No today's sales data found");
                }
            })
            .catch((error) => {
                console.error("Error fetching line chart data:", error);
            });
    };
    
    getLineChartData();






});