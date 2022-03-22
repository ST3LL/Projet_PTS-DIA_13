function get_table_grid(tableID) {
    let tab = document.getElementById(tableID).rows;
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
    submit_grid(grid_id, grid_solved)
    cancelAllAnimationFrames();
}

function submit_grid(grid_id, grid_solved) {
    let grid = get_table_grid(grid_id)
    if (JSON.stringify(grid).replaceAll('"', '') == JSON.stringify(grid_solved)) {
        document.getElementById("win").innerHTML = "Victoire !";
        stop_timer();
    }
    else {
        document.getElementById("win").innerHTML = "La grille n'est pas valide !";
    }
}

