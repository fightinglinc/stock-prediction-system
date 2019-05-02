// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myIndicatorChart");
var myIndiChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: "macd",
      borderColor: "rgb(255,0,0,1)",
      borderWidth: 2,
      pointRadius: 0,
      fill: false,
      data: []
    },{
      type:'line',
      label: "rsi",
      borderColor: "rgb(0,0,255,1)",
      borderWidth: 2,
      pointRadius: 0,
      fill: false,
      data: []
    },



    ],
  },
  options: {
    maintainAspectRatio: false,
    scaleLabel: {
      display: true
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          fontColor: "white",
          maxTicksLimit: 2000
        }
      }],
      yAxes: [{
        ticks: {
          suggestedMin: 1000.00,
          suggestedMax: 0.00
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
