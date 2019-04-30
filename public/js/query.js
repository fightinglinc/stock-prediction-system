$(document).ready(function () {
    $('#updateTime').html("Updated at " + getDate());

    $('#latestPrice').dataTable({
        "ajax": 'http://localhost:5000/latest-price/',
        "processing": true,
        columns: [
            {data: 'name'},
            {data: 'time'},
            {data: 'price'}
        ]
    });

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

        });

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
                {data: 'price'}
            ],

        });

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
    let nowDate = date.getFullYear() + seperator + nowMonth + seperator + strDate;
    return nowDate;
}