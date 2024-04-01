document.addEventListener('DOMContentLoaded', function () {
    const renderChart = (data, labels) => {
        var ctx = document.getElementById('Mypie').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: "Monthly Sales",
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
                        text: 'Monthly Sales'
                    }
                }
            }
        });
    }

    const getLineChartData = () => {
        console.log("Fetching monthly category sales data");
        fetch("/monthly_category_sales/")
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`Failed to fetch data: ${res.status} ${res.statusText}`);
                }
                return res.json();
            })
            .then((results) => {
                console.log("Monthly category sales results", results);
                const monthlySalesData = results.monthly_category_sales;
    
                if (monthlySalesData && typeof monthlySalesData === 'object' && Object.keys(monthlySalesData).length > 0) {
                    const categoryNames = Object.keys(monthlySalesData);
                    const months = Object.keys(monthlySalesData[categoryNames[0]]); // Get months from the first category
                    const data = months.map(month => {
                        return categoryNames.reduce((total, category) => total + (monthlySalesData[category][month] || 0), 0);
                    });
    
                    renderChart(data, months);
                } else {
                    console.error("No monthly category sales data found");
                }
            })
            .catch((error) => {
                console.error("Error fetching monthly category sales data:", error);
            });
    };
    
    getLineChartData();
});