document.addEventListener('DOMContentLoaded', function () {
    const renderChart = (data, labels) => {
        var ctx = document.getElementById('myLine').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: "Today's Sales",
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
                        text: "Today's Sales"
                    }
                }
            }
        });
    }

    const getChartData = () => {
        console.log("fetching");
        fetch("/income/user_income_list/")
            .then((res) => res.json())
            .then((results) => {
                console.log("results", results);
                const source_data = results.income_source_data;
                const [labels, data] = [
                    Object.keys(source_data),
                    Object.values(source_data),
                ];

                renderChart(data, labels);
            });
    };

    getChartData(); // Call getChartData directly after DOMContentLoaded
});