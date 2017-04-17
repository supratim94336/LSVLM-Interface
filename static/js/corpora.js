/*
    Javascript functions for the corpus index
    and the "Add Corpus" form
*/

$(document).ready(function(){    
    
    // Toggle the open/close arrow for the add corpus form
    $('#addCorpusForm').on('show.bs.collapse', function (e) {
        if (e.target === this) {
            $("#expand-arrow").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
       }
    });

    $('#addCorpusForm').on('hide.bs.collapse', function (e) {
        if (e.target === this) {
            $("#expand-arrow").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
        }
    });
    
    // Toggle input field for new language name
    $("#id_lang_select").change(function() {
        if ($(this).val() == "new") {
            $("#id_new_lang").closest('.form-group').collapse('show');
        } else {
            $("#id_new_lang").closest('.form-group').collapse('hide');
        }
    });
    
    // Start off with the new language field hidden
    $("#id_new_lang").closest(".form-group").collapse({toggle: false}).addClass("collapse");
    $("#id_lang_select").change()
    
    // Go to corpus after clicking on table row
    $(".corpus").click(function() {
        window.location = $(this).attr('href');
    });
    
    $(".searchable-table").dataTable();
    
    // enable file path/location or file upload depending on
    // radio button selected
    $("#id_path_type_0, #id_path_type_1").change(updateRadio)
    
});

function updateRadio() {
    if($("#id_path_type_0").is(':checked')) {
        $("#id_file_name").prop('disabled', false);
        $("#id_location").prop('disabled', false);
        $("#id_upload_path").prop('disabled', true);
    }
    else if($("#id_path_type_1").is(':checked')) {
        $("#id_file_name").prop('disabled', true);
        $("#id_location").prop('disabled', true);
        $("#id_upload_path").prop('disabled', false);
    }
}