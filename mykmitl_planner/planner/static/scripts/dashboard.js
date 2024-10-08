


document.addEventListener('DOMContentLoaded', function () {
    fetch('confirmed_bookings/', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const allMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const ctx = document.getElementById('confirmedBookingsChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: allMonths,  // แสดงทุกเดือน
                datasets: [{
                    label: 'Confirmed Bookings Student',
                    data: data.data,  // ข้อมูลจาก backend
                    borderColor: 'rgba(255, 133, 0, 0.8)',
                    backgroundColor: 'rgba(255, 163, 64, 0.8)',
                    fill: true,
                    tension: 0.1,
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: {
                            autoSkip: false,  // บังคับให้แสดงทุกเดือน
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));
});

