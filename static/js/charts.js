// Fetch data from Flask backend and create charts
fetch('/api/bin-stats')
  .then(response => response.json())
  .then(data => {
    const ctx1 = document.getElementById('statusChart');

    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: ['Urgent', 'Medium', 'Good'],
        datasets: [{
          label: 'Number of Bins',
          data: [data.urgent, data.medium, data.good],
          backgroundColor: ['#dc3545', '#ffc107', '#28a745']
        }]
      }
    });

    // PIE chart (optional)
    const ctx2 = document.getElementById('pieChart');
    new Chart(ctx2, {
      type: 'pie',
      data: {
        labels: ['Urgent', 'Medium', 'Good'],
        datasets: [{
          data: [data.urgent, data.medium, data.good],
          backgroundColor: ['#dc3545', '#ffc107', '#28a745']
        }]
      }
    });
  });
