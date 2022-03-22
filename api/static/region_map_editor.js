function showRegionMap(grid, chars, colors, region_map){
    let gridHTML = '';
    chars_str = str_list(chars, false)
    colors_str = str_list(colors, false)
    region_map_str = str_list(region_map, true)

    for (let row = 0; row < grid.length; row++){
        gridHTML += '<tr>';
        for (let col = 0; col < grid[row].length; col++){
            gridHTML += '<td contenteditable="false" id="' + ((row * grid[row].length)+col+1) + '" onclick="select_cell(this, ' + colors_str + ', ' + region_map_str + ');" style="background-color: ' + colors[region_map[row][col]] + 'a0;">' + grid[row][col] + '</td>'
        }
        gridHTML += '</tr>';
    }
    document.getElementById('sudoku_grid').innerHTML = gridHTML;
    document.getElementById('selection_mode').innerHTML = document.getElementById('selection_mode').innerHTML.replace("Simple", "Multi");
    selected = [];
    multi_selection = false;
}




function verify_region(dim){
    var dict = new Map()
    let table = []
    full_dim = dim*dim
    for (let row = 0; row < full_dim; row++){
        let sub_table = []
        for (let col = 0; col < full_dim; col++){
            var val = parseInt(document.getElementById(((row * full_dim)+col+1)).innerHTML)
            sub_table.push(val)
            to_add = 1
            if (dict.has(val) == true){
                to_add += dict.get(val)
            }
            dict.set(val, to_add)
        }
        table.push(sub_table)
    }

    console.log(dict)
    console.log(table)

    for (const [key, value] of dict) {
        if (value != full_dim){
            document.getElementById('win').innerHTML = "Les regions ne sont pas toutes de la bonne taille (" + full_dim + ")";
            return false
        }
    }
    document.getElementById("hidden_table").value = table;
    return true
}