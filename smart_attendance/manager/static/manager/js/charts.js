/**
 * Smart Attendance System - Chart Utilities for Manager Dashboard
 */

// Create attendance trend chart
function createAttendanceTrendChart(elementId, data) {
    const ctx = document.getElementById(elementId);
    
    if (!ctx || typeof Chart === 'undefined') return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Attendance Rate (%)',
                data: data.values,
                backgroundColor: 'rgba(13, 110, 253, 0.2)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: 'rgba(13, 110, 253, 1)',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 10,
                    bodyFont: {
                        size: 14
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Create class distribution pie chart
function createClassDistributionChart(elementId, data) {
    const ctx = document.getElementById(elementId);
    
    if (!ctx || typeof Chart === 'undefined') return;
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(199, 199, 199, 0.8)'
                ],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        boxWidth: 12
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 10,
                    bodyFont: {
                        size: 14
                    }
                }
            }
        }
    });
}

// Create student status bar chart
function createStudentStatusChart(elementId, data) {
    const ctx = document.getElementById(elementId);
    
    if (!ctx || typeof Chart === 'undefined') return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Students',
                data: data.values,
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)',  // Present - green
                    'rgba(220, 53, 69, 0.7)',   // Absent - red
                    'rgba(255, 193, 7, 0.7)',   // Late - yellow
                    'rgba(108, 117, 125, 0.7)'  // Excused - gray
                ],
                borderColor: [
                    'rgb(40, 167, 69)',
                    'rgb(220, 53, 69)',
                    'rgb(255, 193, 7)',
                    'rgb(108, 117, 125)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

// Initialize charts when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Example usage - these would be populated with real data from the backend
    // You would typically pass this data from your Django view to the template
    
    // Check if chart elements exist before trying to create charts
    if (document.getElementById('attendanceTrendChart')) {
        const attendanceTrendData = {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            values: [85, 82, 88, 90, 87]
        };
        createAttendanceTrendChart('attendanceTrendChart', attendanceTrendData);
    }
    
    if (document.getElementById('classDistributionChart')) {
        const classDistributionData = {
            labels: ['Class A', 'Class B', 'Class C', 'Class D'],
            values: [30, 25, 20, 15]
        };
        createClassDistributionChart('classDistributionChart', classDistributionData);
    }
    
    if (document.getElementById('studentStatusChart')) {
        const studentStatusData = {
            labels: ['Present', 'Absent', 'Late', 'Excused'],
            values: [42, 8, 5, 3]
        };
        createStudentStatusChart('studentStatusChart', studentStatusData);
    }
});
