// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
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
    },{
      label: "movingAvg_5",
      borderColor: "rgb(0,255,0,1)",
      borderWidth: 1,
      pointRadius: 0,
      fill: false,
      data: []
    },{
      label: "movingAvg_50",
      borderColor: "rgb(255,180,0,1)",
      borderWidth: 1,
      pointRadius: 0,
      fill: false,
      data: []
    },



    ],
  },
  options: {
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
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
    // legend: {
    //   display: false
    // }
  }
});
