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
      label: "masd",
      borderColor: "rgb(0,255,0,1)",
      borderWidth: 1,
      pointRadius: 0,
      fill: false,
      data: []
    },{
      label: "rsi",
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
