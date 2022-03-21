selected = []
multi_selection = false

function choose(val, colors, region_map) {
    if (val == 0)
        val = ''
    for (let cell_id of selected) {
        document.getElementById(cell_id).innerHTML = val
    }
    reset_selected(colors, region_map)
    cancelAllAnimationFrames();
}


function select_cell(cell, colors, region_map){
    id = cell.id

    if (selected.includes(id)) {
        selected.splice(selected.indexOf(id), 1)
        color = get_cell_color(id, colors, region_map)
        cell.style.backgroundColor = color
    } else if (multi_selection) {
        selected.push(id)
        cell.style.backgroundColor = "#87CEFA80"
    } else {
        reset_selected(colors, region_map)
        selected = [id]
        cell.style.backgroundColor = "#87CEFA80"
    }
    cancelAllAnimationFrames();
}


function reset_selected(colors, region_map){
    for (let cell_id of selected) {
        color = get_cell_color(cell_id, colors, region_map)
        document.getElementById(cell_id).style.backgroundColor = color
    }
    selected = []
}


function switch_mode(but, colors, region_map){
    multi_selection = !multi_selection
    if (multi_selection)
        but.innerHTML = but.innerHTML.replace("Multi", "Simple");
    else
        but.innerHTML = but.innerHTML.replace("Simple", "Multi");
    reset_selected(colors, region_map)
    cancelAllAnimationFrames();
}


function get_cell_color(id, colors, region_map){
    for (let row = 0; row < region_map.length; row++){
        for (let col = 0; col < region_map[row].length; col++){
            val = ((row * region_map[row].length)+col+1)
            if (id == val){
                return colors[region_map[row][col]]+'a0'
            }
        }
    }
}