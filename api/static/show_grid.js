function showGrid(grid, chars, colors, region_map){
    let gridHTML = '';
    chars_str = str_list(chars, false)
    colors_str = str_list(colors, false)
    region_map_str = str_list(region_map, true)

    for (let row = 0; row < grid.length; row++){
        gridHTML += '<tr>';
        for (let col = 0; col < grid[row].length; col++){
            if (grid[row][col] == 0){
                gridHTML += '<td contenteditable="false" id="' + ((row * grid[row].length)+col+1) + '" onclick="select_cell(this, ' + colors_str + ', ' + region_map_str + ');" style="background-color: ' + colors[region_map[row][col]] + 'a0;"></td>'
            }else if (grid[row][col])
                gridHTML += '<td contenteditable="false" style="background-color: ' + colors[region_map[row][col]] + '50;">' + grid[row][col] + '</td>'
            else
                gridHTML += '<td contenteditable="false" class="none"></td></td>';
        }
        gridHTML += '</tr>';
    }
    document.getElementById('sudoku_grid').innerHTML = gridHTML;
    document.getElementById('win').innerHTML = "";
    document.getElementById('selection_mode').innerHTML = document.getElementById('selection_mode').innerHTML.replace("Simple", "Multi");
    selected = [];
    multi_selection = false;
    reset_timer();
    cancelAllAnimationFrames();
}
