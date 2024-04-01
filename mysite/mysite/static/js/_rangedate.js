document.addEventListener("DOMContentLoaded", function() {
    // Initialize datepickers
    $('#start-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
    });

    $('#end-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
    });

    // Handle button click to fetch custom data
    document.getElementById('fetch-custom-data').addEventListener('click', function() {
        // Get the start date and end date values
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;

        // Get the CSRF token from the cookie
        const csrftoken = getCookie('csrftoken');

        // Make a fetch request to your endpoint with the selected date range
        fetch("/income/custom_date_range_income/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken // Include the CSRF token in the request headers
            },
            body: JSON.stringify({ start_date: startDate, end_date: endDate })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Custom date range income data:', data);
            // Handle the fetched data as needed
        })
        .catch(error => {
            console.error('Error fetching custom date range income data:', error);
        });
    });
});

// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie contains the CSRF token
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}