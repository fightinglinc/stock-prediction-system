$(document).ready(function () {
    $('#latestPrice').dataTable({
        "ajax": 'http://localhost:5000/latest-price/',
        "processing": true,
        columns: [
            {data: 'name'},
            {data: 'price'},
            {data: 'time'}
        ]
    });
    // $.ajax({
    //     url: 'http://localhost:5000/latest-price/',
    //     method: "GET",
    //     cache: false,
    //     success: function (data) {
    //         $('#latestPrice').dataTable({
    //             "ajax": 'http://localhost:5000/latest-price/',
    //             columns: [
    //                 {data: 'name'},
    //                 {data: 'price'},
    //                 {data: 'time'}
    //             ]
    //         })
    //     }
    // });
});