String.prototype.addSlashes = function() 
{ 
   //no need to do (str+'') anymore because 'this' can only be a string
   return this.replace(/\[/g, '\\\[').replace(/\]/g, '\\\]');
} 

function loadLM(lm_data) {
    
    $("#default-corpus").val(lm_data["default_corpus"])
    delete lm_data["default_corpus"]

    for (var lm_id in lm_data) {
        var lm = lm_data[lm_id]
        
        var lm_block = null;
        if(lm_id == "MainLM") {
            lm_block = $("#MainLM")
            
            // position the LM block
            lm_block.css({position:'absolute',
                          'left':lm['coords'][0],
                          'top':lm['coords'][1]});
            delete lm['coords']
        } else {
            addNewLM(lm_id, lm['coords'][0], lm['coords'][1])
            lm_block = $("#" + lm_id)
            delete lm['coords']
        }
        // select the LM, and manually trigger the change event
        lm_block.find(".lm-select").val(lm['Type']).change();

        if (lm['Type'] == 'Linear' || lm['Type'] == 'LogLinear') {
            for (i = 0; i < (Object.keys(lm).length - 2) / 2; i++)
                lm_block.find(".add-multi-lm").click()
        }
        delete lm['Type']
    }
    for (var lm_id in lm_data) {
        var lm = lm_data[lm_id]
        var lm_block = $("#" + lm_id)
        // iterate over the other fields
        for(var key in lm) {
            var val = lm[key]
            key = key.addSlashes()

            // is either an LM or a corpus
            if(val.constructor === Array) {
                if(val[0] == "lm") {
                    addConnection(lm_block.find(".lm#" + key).find(".add-lm"), val[1])
                }
                else if (val[0] == "corpus") {
                    lm_block.find("select.corpus#" + key).val(val[1]);
                    lm_block.find("input#" + key + "-n").val(val[2]);
                }
            } else { // is a plain input value, so just set it
                lm_block.find("input#" + key).val(val);
            }
        }
    }
    
    drawLines();
}
