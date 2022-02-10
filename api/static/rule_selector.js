function updateRulesSelector(model, d_models){
    l_rules = d_models[model];
    let optionHTML = '';
    for (let r of l_rules){
        /* optionHTML += '<option value="' + r + '">' + r + '</option>'; */
         optionHTML += '<input type="checkbox" id="comp_select2" name="comp_select2" value=value="' + r + '">' + r + '>';
    }
    document.getElementById('comp_select2').innerHTML = optionHTML;
}