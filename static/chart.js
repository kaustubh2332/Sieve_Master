document.addEventListener('DOMContentLoaded', async () => {
    const ctx = document.getElementById('benchmark-chart').getContext('2d');

    try {
        const response = await fetch('/benchmark-data');
        if (!response.ok) {
            throw new Error('Failed to fetch benchmark data.');
        }
        const benchmarkData = await response.json();

        const labels = benchmarkData.algorithms; 
        const executionTimes = benchmarkData.execution_times; 

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Execution Time (seconds)',
                    data: executionTimes,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                    borderColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: (tooltipItem) => {
                                return `${tooltipItem.label}: ${tooltipItem.raw.toFixed(4)} seconds`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Execution Time (seconds)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Algorithms'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load benchmark data. Please try again.');
    }
});
