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
    console.log('-'+JSON.stringify(grid)+'-')
    console.log('-'+JSON.stringify(grid_solved)+'-')

    if (JSON.stringify(grid) == JSON.stringify(grid_solved)) {
        document.getElementById("win").innerHTML = "Victoire !";
    }
    else {
        document.getElementById("win").innerHTML = "La grille n'est pas valide !";
    }
}
