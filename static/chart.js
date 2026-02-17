document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById('categoryChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: window.chartLabels,
            datasets: [{
                data: window.chartData
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

});
