function showGrid(grid, chars){
    let gridHTML = '';
    chars_str = '['
    chars.forEach(function(c) {
        chars_str += "'" + c + "', "
    });
    chars_str = chars_str.substring(0, chars_str.length - 2) + ']'

    for (let row of grid){
        gridHTML += '<tr>';
        for (let col of row){
            if (col == 0)
                gridHTML += '<td contenteditable="true" onKeyUp="verification_value_cell(this, ' + chars_str + ');"></td>'
            else if (col)
                gridHTML += '<td contenteditable="false" style="background-color: #bebebe;">' + col + '</td>'
            else
                gridHTML += '<td contenteditable="false" class="none"></td></td>';
        }
        gridHTML += '</tr>';
    }
    document.getElementById('sudoku_grid').innerHTML = gridHTML;
    document.getElementById('win').innerHTML = "";
    reset_timer();
}
