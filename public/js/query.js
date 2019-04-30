$(document).ready(function () {
    $.ajax({
        url: 'http://localhost:5000/latest-price/',
        method: "GET",
        cache: false,
        success: function (data) {
            $('#latestPrice').DataTable({
                data: data,
                columns: [
                    {data: 'id'},              
                    {data: 'nickname'},
                    {data: 'phonenumber'}
                ]
            });
        }
    });
});