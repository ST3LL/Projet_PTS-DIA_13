function showSolution(grid_solved){
    let gridHTML = '';
    for (let row of grid_solved){
        gridHTML += '<tr>';
        for (let col of row){
            gridHTML += '<td>'+ col +'</td>';
        }
        gridHTML += '</tr>';
    }
    document.getElementById('sudoku_grid').innerHTML = gridHTML;
    stop_timer();
}