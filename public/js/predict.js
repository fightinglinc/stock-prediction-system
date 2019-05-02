$(document).ready(function () {
    $('#selectCompany').change(function () {
        let company = $('#selectCompany').val();

        $('#predictPrice').dataTable({
            "ajax": 'http://localhost:5000/predict/' + company,
            "processing": true,
            "lengthChange": false,
            "info": false,
            "searching": false,
            "paging": false,
            "bDestroy": true,
            columns: [
                {data: 'algorithm'},
                {data: 'price'},
            ],
        }).on('xhr.dt', function (e, settings, json, xhr) {
            if (xhr.status === 0) {
                swal("Not exist", "Please select another stock", "warning");
                $('#lowPrice tbody').html('');
            }
        });
    });
});