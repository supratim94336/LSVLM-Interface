$(document).ready(function(){    
    $(".corpus").click(function() {
        window.location = $(this).attr('href');
    });
    $(".searchable-table").dataTable();
});