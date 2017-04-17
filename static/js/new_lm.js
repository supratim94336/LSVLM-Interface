counter = 2;

$(document).ready(function(){
    // add the first LM
    var newDivContent = $("#template-lm-box").html().replace(/template-lm/g, "MainLM");
    var newDiv = $(newDivContent);
    newDiv.find(".pre-title").html("Main LM")
    newDiv.find(".delete").remove()
    $("#lm-blocks").append(newDiv)
    
    // fill in the <select> template for the first LM and activate jQuery
    $(".lm-select").html($("#template-select").html());
    updateJQuery($(".lm-block"))
    
    // update the template when the above <select> changes
    $(".lm-select").change(function() {
        updateLMSelect($(this));
    })
    
    $("#addLMForm").submit(function(e) {
       return submitForm();
    })
    
    // Remove error class when we enter valid input
    $("#lm-blocks").on("keyup change", ".lm-field.form-error", function() {
        $(this).removeClass("form-error");
        validateLMField($(this), {});
        
    })
    
    $("#lm-blocks").on("change", ".lm-selector.form-error", function () {
        $(this).removeClass("form-error");
        validateLMSelector($(this));
    });
    
    // Select a default corpus
    $("#default-corpus").on("change", function() {
        corpus_id = $(this).val();
        $(".lm-template").each(function () {
            template = $("<div>") // use a div so that we can manipulate the element
            template.html($(this).html())
            template.find("select.corpus option").removeAttr("selected").filter("[value='" + corpus_id + "']").attr("selected", "selected")
            $("#" + $(this).attr("id")).html(template.html())
            $("select.corpus:has(option[value='0']:selected)").val(corpus_id)
        })
    });

});

// Update the LM template when a new LM type is selected from the <select> element
function updateLMSelect(element) {
    template_name = "#template-" + $(element).val();
    par = $(element).closest(".lm-block");
    $(par).find(".add-lm").each(function() {
        deleteConnection($(this))
    });
    if(template_name == "#template-0") {
        $(par).find(".lm-fields").html("");
        $(par).find(".title").html("");
    } else {
        $(par).find(".lm-fields").html($(template_name).html().replace(/template-lm/g, par.attr("id")));
        $(par).find(".title").html(" : " + $(element).find("option:selected").text())
        updateJQuery(par)
    }
}

// After adding a new LM, update all of the jQuery
function updateJQuery(element){
    
    // make the LM itself draggable
    $(element).draggable({
        cancel : ".add-lm, input, select",
        drag: function(event, ui){ drawLines(); }
    });
    
    // Add more LM links for a LM that supports any number of other LMs
    $(element).find(".add-multi-lm").click(function() {
        newLM = $($("#template-add-lm-many").html())
        $(this).siblings(".lm-many").append(newLM)
        var interpsize = $(this).siblings(".lm-many").children().length - 1
        $(newLM).attr('id', "LM[" + interpsize.toString() + "]");
        $(newLM).find(".float").attr('id', "Weight[" + interpsize.toString() + "]");
        addLMDraggable($(newLM).find(".add-lm"))
        $(newLM).find(".delete-from-list").click(function() {
            $(this).siblings(".add-lm").remove()
            $(this).siblings(".float").remove()
            $(this).remove()
            drawLines();
            //$(newLM).find(".add-lm").remove()
            //$(newLM).find(".delete-from-list").remove()
        })
    });
    
    // dragging the "add-lm" box to add a new connection
    $(element).find(".add-lm").each(function() {
       addLMDraggable($(this)) 
    });
    
    // Activate tooltips
    $(element).find('[data-toggle="tooltip"]').tooltip()
    
    // Change arrow on collapse of LM blocks
    $(element).find('.collapse').on('shown.bs.collapse', function (e) {
        if (e.target === this) {
            $(this).closest(".collapser").find(".expand-arrow").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
            drawLines();
       }
    });

    $(element).find('.collapse').on('hidden.bs.collapse', function (e) {
        if (e.target === this) {
            $(this).closest(".collapser").find(".expand-arrow").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
            drawLines();
        }
    });
    
    // Delete the element and remove the link to the previous element
    $(element).find(".panel-heading .delete").click(function () {
        linked = $(".add-lm[href=" + $(this).closest(".lm-block").attr("id") + "]");
        deleteConnection(linked)
        $(element).remove()
    });
}

function addLMDraggable(element) {
    $(element).draggable({
        helper: function(event) {
            var newDivContent = $("#template-helper").html()
            var newDiv = $(newDivContent);
            newDiv.attr("id", "lm-" + counter);
            $(this).attr("href", newDiv.attr("id"));
            return $(newDiv);
        },
        drag: function(event, ui){
            // react to snapping/unsnapping
            var draggable = $(this).data("ui-draggable")
            var snapped = false;
            $.each(draggable.snapElements, function(index, element) {
                if(element.snapping){
                    snapped = element.item;
                }
            });
            
            if(snapped && !$(this).data().hasOwnProperty("snapElement")) {
                $(this).data("snapElement", $(snapped).attr("id"));
                $(ui.helper).addClass("snapped")
            }
            
            if(!snapped && $(this).data().hasOwnProperty("snapElement")) {
                $(this).removeData("snapElement");
                $(ui.helper).removeClass("snapped")
            }
            
            drawLines();
        },
        snap: ".lm-block-snappable:not('#" + $(element).closest(".lm-block").attr("id") + "-snappable')",
        snapMode: "outer",
        // Put down a new LM in the canvas
        stop: function(event, ui) {
          // just add a connection to the existing element if snapped
          if($(this).data().hasOwnProperty("snapElement")) {
              id = $("#" + $(this).data("snapElement")).closest(".lm-block").attr("id")
          }
          // otherwise, create a new LM box where we dropped the cursor
          else {
              id = $(this).attr("href");
              addNewLM(id, ui.offset.left, ui.offset.top)
          }
          
          addConnection($(this), id)
          drawLines();
        }
    });
}

// Add a connection from a source .add-lm to a target id
function addConnection(source, target) {
    source.attr("href", target)
    source.draggable("disable")
    source.addClass("glyphicon-remove")
    source.removeClass("glyphicon-plus")
    source.click(function () {
        deleteConnection($(this))
    });
}

// Create a new LM with the given id and position coordinates
function addNewLM(id, left, top) {
    // if we are editing an LM, we want to make sure we don't repeat ids
    while($("#" + id).length > 1) {
        counter++;
        id = "lm-" + counter;
    }
    
    var newDivContent = $("#template-lm-box").html().replace(/template-lm/g, id);
    var newDiv = $(newDivContent);
    newDiv.css({position:'absolute',
            'left':left,
            'top':top});
    counter++;

    newDiv.find(".lm-select").html($("#template-select").html());
    
    newDiv.find(".lm-select").change(function () {
        updateLMSelect($(this));
    })
    updateJQuery(newDiv)
    $("#lm-blocks").append(newDiv);
}

// Remove the outward connection from a given .add-lm element
function deleteConnection(element) {
    element.removeAttr("href");
    element.unbind('click');
    element.addClass("glyphicon-plus")
    element.removeClass("glyphicon-remove")
    element.draggable("enable");
    drawLines();
}

// Draw the lines between language models by iterating over the "href" of each LM property
function drawLines() {
    var c=document.getElementById("lm-canvas");
    var ctx=c.getContext("2d");
    
    $(".lm-block").data("num_outgoing", 0);
    $(".lm-block").data("num_incoming", 0);
    
    // figure out how big to make the canvas
    $(".add-lm").each(function (index){
        if(!$(this).attr("href")) {
            return;
        }
        var origin = $(this).offset();
        var target = $("#" + $(this).attr("href")).offset();
        
        c.width = Math.max(target.left, c.width, origin.left + $(this).closest(".panel-body").width());
        c.height = Math.max(target.top + 500, c.height, origin.top);
    });
    
    ctx.clearRect (0, 0 , c.width, c.height);
    
    $(".add-lm").each(function (index){
        if(!$(this).attr("href")) {
            return;
        }
        
        var origin = $(this).offset();
        var lmBlock = $(this).closest(".lm-block")
        var target = $("#" + $(this).attr("href"))
        var target_coords = target.offset()
        var edge_distance = 30;
        
        var num_outgoing = $(this).closest(".lm-block").data("num_outgoing");
        var num_incoming = target.closest(".lm-block").data("num_incoming");
        $(this).closest(".lm-block").data("num_outgoing", num_outgoing + 1)
        target.closest(".lm-block").data("num_incoming", num_incoming + 1)
        
        // check if the LM box is closed
        if(!$(this).closest(".panel-body").hasClass("in")) {
            origin.top = lmBlock.offset().top + lmBlock.height()/2 - 10 + num_outgoing*10;
            origin.left = lmBlock.offset().left + lmBlock.width();
        }
        // check if it is optional and the option box is closed
        else if($(this).closest(".optional-fields:not(.in)").length > 0) {
            origin.top = $(this).closest(".optional").offset().top + num_outgoing*10;
            origin.left = lmBlock.offset().left + lmBlock.width();
        }
        else {
            origin.top = origin.top + 15;
            origin.left = origin.left + 50;
        }
        
        // first, draw to edge of panel body + edge_distance
        var firstpt = {}
        firstpt.x = lmBlock.offset().left + lmBlock.width() + edge_distance + num_outgoing*20;
        firstpt.y = origin.top
        
        ctx.beginPath()
        ctx.moveTo(origin.left, origin.top);
        ctx.lineTo(firstpt.x, firstpt.y);

        // then find the end point on the target panel
        targetpt = {}
        endpt = {}
        
        endpt.x = target_coords.left
        targetpt.x = endpt.x - edge_distance;

        // figure out where to place the X coordinate
        if(target.height() < 70) {
            targetpt.y = target_coords.top + target.height()/2 - 10
        } else {
            targetpt.y = target_coords.top + 35;
        }
        targetpt.y = targetpt.y + num_incoming*7
        endpt.y = targetpt.y
            
        // if the target panel is to the right of the source panel,
        // just extend the line from the source panel and then draw a straight
        // up/down line
        if (targetpt.x > firstpt.x) {
            ctx.lineTo(targetpt.x, firstpt.y);
        }
        // if the target panel is below and to the left of the source panel
        else if(targetpt.y > firstpt.y) {
            // if there is a space between the source and target, draw the line between them
            if ((lmBlock.offset().top + lmBlock.height() + edge_distance) < target.offset().top) {
                ctx.lineTo(firstpt.x, lmBlock.offset().top + lmBlock.height() + edge_distance);
                ctx.lineTo(targetpt.x, lmBlock.offset().top + lmBlock.height() + edge_distance)
            }
            // otherwise, draw the lines going around the other way
            else {
                ctx.lineTo(firstpt.x, lmBlock.offset().top + lmBlock.height() + edge_distance)
                ctx.lineTo(targetpt.x, lmBlock.offset().top + lmBlock.height() + edge_distance)
            }
        } else {
            // if there is a space between the target and source, draw the line between them
            if ((target.offset().top + target.height() + edge_distance) < lmBlock.offset().top) {
                ctx.lineTo(firstpt.x, target.offset().top + target.height() + edge_distance);
                ctx.lineTo(targetpt.x, target.offset().top + target.height() + edge_distance)
            } else {
                ctx.lineTo(firstpt.x, lmBlock.offset().top - edge_distance)
                ctx.lineTo(targetpt.x, lmBlock.offset().top - edge_distance)
            }
        }
        
        ctx.lineTo(targetpt.x, targetpt.y);
        
        ctx.lineTo(endpt.x, endpt.y)
        ctx.stroke();
        ctx.closePath();
        
        // draw arrow at target element
        ctx.beginPath();
        ctx.moveTo(endpt.x - 8, endpt.y - 8);
        ctx.lineTo(endpt.x, endpt.y);
        ctx.lineTo(endpt.x - 8, endpt.y + 8);
        ctx.closePath();
        ctx.fill()
    });

}

// Check that the LM type dropdown has a valid value
function validateLMSelector(select) {
    var lm_id = select.find(".lm-select").val();
    if (lm_id == "0") {
        select.addClass("form-error")
    }
}

// Check that a .lm-field has a valid value
function validateLMField(field, lm) {
    required = (field.closest(".optional").length < 1)
    var errors = false;
    
    if(field.hasClass("text")){
        var input = field.find("input")
        var val = input.val()
        if(val.length > 0){
            lm[input.attr("id")] = val
        } else if(required) {
            field.addClass("form-error")
            errors = true;
            field.find(".error").html("Please enter a valid string.");
        }
    }
    else if(field.hasClass("int")) {
        var input = field.find("input")
        var val = input.val()
        var int = parseInt(val)
        if(!isNaN(int) && int >= 0){
            lm[input.attr("id")] = parseInt(val)
        } else if(required) {
            field.addClass("form-error")
            errors = true;
        }
    }
    else if(field.hasClass("float")) {
        var input = field.find("input")
        var val = input.val()
        var float = parseFloat(val)
        if(!isNaN(float) && float >= 0){
            lm[input.attr("id")] = parseFloat(float)
        } else if(required) {
            field.addClass("form-error")
            errors = true
        }
    }
    else if(field.hasClass("lm")) {
        var target_lm_id = field.find(".add-lm").attr("href");
        if (target_lm_id && target_lm_id.length > 0){
            lm[field.attr("id")] = ["lm", target_lm_id];
        } else if (required) {
            field.addClass("form-error")
            errors = true;
        }
    }
    else if(field.hasClass("lm-many")) {
	var index = 0;
        var memberlms = field.find(".add-multi-lm").siblings()[0].children
        for (var i = 0; i < memberlms.length; i++) {
            var innerlm = memberlms[i];
            //if (innerlm.find(".add-lm")) {
                var input = innerlm.children[1]
                var val = input.value
                var float = parseFloat(val)
                if(!isNaN(float) && float >= 0){
                    lm["Weight[" + index.toString() + "]"] = parseFloat(float)
                } else {
                    field.addClass("form-error")
                    errors = true
                }
                var target_lm = innerlm.children[2]
                if (target_lm.attributes.length > 1){
                    var target_lm_id = target_lm.attributes[1].value;
                } else {
                    var target_lm_id = false;
                }
                if (target_lm_id && target_lm_id.length > 0){
                    lm["LM[" + index.toString() + "]"] = ["lm", target_lm_id];
                } else {
                    field.addClass("form-error")
                    errors = true;
                }
                index = index + 1;
            //}
        }
    } 
    else if(field.hasClass("corpus")) {
        var corpus_select_id = field.attr("id")
        var corpus_id = field.find(".corpus").val()
        if(corpus_id != "" && corpus_id != "0") {
            lm[corpus_select_id] = ["corpus", corpus_id]
        } else if (required) {
            field.addClass("form-error")
            field.find(".error").html("Please select a corpus.");
            errors = true;
        }
    }
    return errors;
    
}

function submitForm(e) {
    lms = {};
    
    $(".form-error").removeClass("form-error")
    $(".error").html("")
    var errors = false;
    
    // iterate over each LM
    $(".lm-block").each(function() {
        var lm_data = {}
        var id = $(this).attr("id");
        var lm_id = $(this).find(".lm-select").val();
        if (lm_id == "0") {
            $(this).find(".lm-selector").addClass("form-error")
            errors = true;
        }
        lm_data["Type"] = lm_id
        
        // add each field within the LM
        $(this).find(".lm-field").each(function() {
            errors = validateLMField($(this), lm_data) || errors;
        });
        
        lm_data['coords'] = [$(this).offset().left, $(this).offset().top];
        
        lms[id] = lm_data;
    });
    
    if(errors) {
        return false;
    }
    
    json = JSON.stringify([lms]);
    $("#lm_json").val(json);
    return true;

}
