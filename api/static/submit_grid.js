function get_table_grid(tableID) {
    let tab = document.getElementById(tableID).rows;
    console.log(tableID)
    console.log(tab)
    tab_list = []
    for (var i = 0; i < tab.length; i++) {
            elem = tab[i].children
            my_elem = []
            for (let j = 0; j < elem.length; j++) {
                    my_elem.push(elem[j].innerText.replace('\n', ''));
            }
            tab_list.push(my_elem)
    }
    return tab_list

}

function submit_sudoku(grid_id, grid_solved) {
    let grid = get_table_grid(grid_id)
    console.log(grid)
    console.log(grid_solved)
    console.log('-'+JSON.stringify(grid).replaceAll('"', '')+'-')
    console.log('-'+JSON.stringify(grid_solved)+'-')

    if (JSON.stringify(grid).replaceAll('"', '') == JSON.stringify(grid_solved)) {
        document.getElementById("win").innerHTML = "Victoire !";
        stop_timer();
    }
    else {
        document.getElementById("win").innerHTML = "La grille n'est pas valide !";
    }
}


function verification_value_cell(cell, chars){
    console.log(chars)
    console.log(chars)
    val_cell = cell.innerHTML.replace('<br>', '')
    if (!(chars.includes(val_cell))) {
        cell.innerHTML = '<br>'
    }
}