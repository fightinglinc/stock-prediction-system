// written by: Kuo-Wei Chung
// assisted by: Kuo-Wei Chung
// debugged by: All members
$(document).ready(function () {
    $('#updateTime').html("Updated at " + getDate());

    // Query 1: latest price
    $('#latestPrice').dataTable({
        "ajax": 'http://localhost:5000/latest-price/',
        "processing": true,
        stateSave: true,
        columns: [
            {data: 'name'},
            {data: 'time'},
            {data: 'price'},
            {data: 'volume'}
        ]
    });

    // Query 2: Highest Stock Price
    $('#searchButton').click(function () {
        let company = $('#searchAnyCompany').val();

        $('#highPrice').dataTable({
            "ajax": 'http://localhost:5000/high-price/' + company,
            "processing": true,
            "lengthChange": false,
            "info": false,
            "bSort": false,
            "searching": false,
            "paging": false,
            "bDestroy": true,
            columns: [
                {data: 'name'},
                {data: 'time'},
                {data: 'price'}
            ],
        }).on('xhr.dt', function (e, settings, json, xhr) {
            if (xhr.status === 0) {
                swal("Not exist", "Please enter another stock", "warning");
                $('#highPrice tbody').html('');
            }
        });
    });

    // Query 3: Average Stock Price
    $('#searchButton2').click(function () {
        let company = $('#searchAnyCompany2').val();

        $('#avgPrice').dataTable({
            "ajax": 'http://localhost:5000/avg-price/' + company,
            "processing": true,
            "lengthChange": false,
            "info": false,
            "bSort": false,
            "searching": false,
            "paging": false,
            "bDestroy": true,
            columns: [
                {data: 'name'},
                {data: 'price'}
            ],
        }).on('xhr.dt', function (e, settings, json, xhr) {
            if (xhr.status === 0) {
                swal("Not exist", "Please enter another stock", "warning");
                $('#avgPrice tbody').html('');
            }
        });
    });

    // Query 4: Lowest Stock Price
    $('#searchButton3').click(function () {
        let company = $('#searchAnyCompany3').val();

        $('#lowPrice').dataTable({
            "ajax": 'http://localhost:5000/low-price/' + company,
            "processing": true,
            "lengthChange": false,
            "info": false,
            "bSort": false,
            "searching": false,
            "paging": false,
            "bDestroy": true,
            columns: [
                {data: 'name'},
                {data: 'time'},
                {data: 'price'}
            ],
        }).on('xhr.dt', function (e, settings, json, xhr) {
            if (xhr.status === 0) {
                swal("Not exist", "Please enter another stock", "warning");
                $('#lowPrice tbody').html('');
            }
        });
    });

    // Query 5: List company
    $('#selectCompany').change(function () {
        let company = $('#selectCompany').val();

        $('#listCompany').dataTable({
            "ajax": 'http://localhost:5000/list-company/' + company,
            "processing": true,
            "lengthChange": false,
            "info": false,
            "searching": false,
            "paging": false,
            "bDestroy": true,
            columns: [
                {data: 'id'},
                {data: 'name'},
                {data: 'price'}
            ],

        });
    });
});

function getDate() {
    let date = new Date();
    let nowMonth = date.getMonth() + 1;
    let strDate = date.getDate();
    let seperator = "-";

    if (nowMonth >= 1 && nowMonth <= 9) {
        nowMonth = "0" + nowMonth;
    }

    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    return date.getFullYear() + seperator + nowMonth + seperator + strDate;
}