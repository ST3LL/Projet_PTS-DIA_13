function showSolution(grid_solved, colors, region_map){
    let gridHTML = '';
    for (let row = 0; row < grid_solved.length; row++){
        gridHTML += '<tr>';
        for (let col = 0; col < grid_solved[row].length; col++){
            gridHTML += '<td style="background-color: ' + colors[region_map[row][col]] + '50;">'+ grid_solved[row][col] +'</td>';
        }
        gridHTML += '</tr>';
    }
    document.getElementById('sudoku_grid').innerHTML = gridHTML;
    stop_timer();
}