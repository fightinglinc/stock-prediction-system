$(document).ready(function () {
    $('#selectCompany, #selectTerm').change(function () {

        let company = $('#selectCompany').val();
        let term = $('#selectTerm').val();

        if (company && term) {
            $('#predictPrice').dataTable({
                "ajax": 'http://localhost:5000/predict/' + company + '/' + term,
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
                    $('#predictPrice tbody').html('');
                }
            });
        }
    });
});