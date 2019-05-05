// written by: Kuo-Wei Chung
// assisted by: Kuo-Wei Chung
// debugged by: All members
(function($) {
  "use strict"; // Start of use strict
  // datepicker
  $('.input-daterange input').each(function() {
      $(this).datepicker('clearDates');
  });
  // Toggle the side navigation
  $("#sidebarToggle").on('click', function(e) {
    e.preventDefault();
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });



  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    event.preventDefault();
  });



  $('#addNewStockButton').click(function() {
  //Send the AJAX call to the server
    console.log("QQQ");
    var newStock = $('#addNewStockField').val();
    console.log(newStock);
    $.ajax({
      'url' : 'http://localhost:5000/historical-stock-data/' + newStock,
      'type' : 'PUT',
      'beforeSend': function(){
        $("#loader").show();
       },
      'success': function(data) {
      },
      'complete': function() {
        $("#loader").hide();
      }
    });
    $.ajax({
      'url' : 'http://localhost:5000/realtime-stock-data/' + newStock,
      'type' : 'PUT',
      'beforeSend': function(){
        $("#loader").show();
       },
      'success': function(data) {
      },
      'complete': function() {
        $("#loader").hide();
      }
    });
  });

  $('#searchStockByPeriodButton').click(function() {
    var company = document.getElementById('searchByStockName').value;
    var from = document.getElementById('dateFrom').value;
    var to = document.getElementById('dateTo').value;

    $.ajax({
      'url' : 'http://localhost:5000/historical-stock-data/' + company + '?' + 'from=' + from + '&to=' + to,
      'type' : 'GET',
      'success' : function(data) {
        var stockData = JSON.parse(data);
        addDataToPriceChart(myLineChart, stockData['dates'], stockData['prices'], stockData['movingAvgShort'], stockData['movingAvgLong']);
        addDataToIndicatorChart(myIndiChart, stockData['dates'], stockData['macd'], stockData['rsi']);

      }
    });
  });




    $('#searchRealtimeStockButton').click(function() {
      var company = document.getElementById('searchByRealtimeStockName').value;
      $.ajax({
        'url' : 'http://localhost:5000/realtime-stock-data/' + company,
        'type' : 'GET',
        'success' : function(data) {
          var stockData = JSON.parse(data);
          addDataToRealtimeChart(myRealtimeLineChart, stockData['times'], stockData['prices']);
        }
      });
    });


  function addDataToRealtimeChart(chart, times, prices) {
    chart.data.labels = times;
    chart.data.datasets[0].data = prices;
    chart.update();
  }

  function addDataToPriceChart(chart, dates, prices, movingAvgShort, movingAvgLong) {
    chart.data.labels = dates;
    chart.data.datasets[0].data = prices;
    chart.data.datasets[1].data = movingAvgShort;
    chart.data.datasets[2].data = movingAvgLong;
    chart.update();
  }


    function addDataToIndicatorChart(chart, dates, macd, rsi) {
      chart.data.labels = dates;
      chart.data.datasets[0].data = macd;
      chart.data.datasets[1].data = rsi;
      chart.update();
    }




})(jQuery); // End of use strict
