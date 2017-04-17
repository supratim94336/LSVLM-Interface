$(document).ready(function () {

    // Toggle the open/close arrow for the run experiment form
    $('#addExpSetForm').on('show.bs.collapse', function (e) {
        if (e.target === this) {
            $("#expand-arrow").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
       }
    });

    $('#addExpSetForm').on('hide.bs.collapse', function (e) {
        if (e.target === this) {
            $("#expand-arrow").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
        }
    });

    /*$("#add-lm").click(function() {
        $("#lms").append($("#template-add-lm").html())
    });
    
    $("#add-corpus").click(function() {
        $("#corpora").append($("#template-add-corpus").html())
    });
    
    $("#corpora,#lms").on("click", '.remove', function() {
        $(this).closest(".row").remove()
    });*/
    
    $(".corpus").click(function() {
        window.location = $(this).attr('href');
    });
    
    $(".searchable-table").dataTable();

    // enable file path/location or file upload depending on
    // radio button selected
    $("#id_source_0, #id_source_1").change(updateRadio)

});

/*function pageInit() {
    if (document.getElementById("corpus_radio").checked) {
        document.getElementById("corpus").disabled = false;
        document.getElementById("corpus").focus();
    }
}

function selectCorpus() {
    document.getElementById("errorMsg").innerHTML = "";
    document.getElementById("corpus").disabled = false;
}

function selectInputTextArea() {
    document.getElementById("input_text").focus();
    document.getElementById("input_text_radio").checked = "checked";
    document.getElementById("corpus").disabled = true;
}

function validate() {
    if (document.getElementById("input_text_radio").checked)
        if ((document.getElementById("input_text").value).trim() == '') {
            document.getElementById("errorMsg").style.color = 'red';
            document.getElementById("errorMsg").innerHTML = "Please enter a non-empty input text to continue."
            document.getElementById("input_text").value = '';
            return false;
        }
    return true;
}*/

function updateRadio() {
    if($("#id_source_0").is(':checked')) {
        $("#id_corpus").prop('disabled', false);
        $("#id_input_text").prop('disabled', true);
    }
    else if($("#id_source_1").is(':checked')) {
        $("#id_corpus").prop('disabled', true);
        $("#id_input_text").prop('disabled', false);
    }
}
