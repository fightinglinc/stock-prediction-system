// written by: Kuo-Wei Chung
// assisted by: Kuo-Wei Chung
// debugged by: Linchen Xie
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myRealtimeAreaChart");
var myRealtimeLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: "price",
      borderColor: "rgba(2,117,216,0.8)",
      pointRadius: 0.5,
      pointBackgroundColor: "rgba(2,117,216,0.8)",
      pointBorderColor: "rgba(2,117,216,0.8)",
      pointBorderWidth: 3,
      fill: false,
      data: []
    }],
  },
  options: {
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        time: {
          unit: 'hour'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 2000
        }
      }],
      yAxes: [{
        ticks: {
          suggestedMin: 2000,
          suggestedMax: 0
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
