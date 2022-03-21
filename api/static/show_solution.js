function showSolution(grid_solved, colors, region_map){
    let gridHTML = '';
    for (let row = 0; row < grid_solved.length; row++){
        gridHTML += '<tr>';
        for (let col = 0; col < grid_solved[row].length; col++){
            gridHTML += '<td id="' + ((row * grid_solved[row].length)+col+1) + '" style="background-color: ' + colors[region_map[row][col]] + '50;">'+ grid_solved[row][col] +'</td>';
        }
        gridHTML += '</tr>';
    }
    document.getElementById('sudoku_grid').innerHTML = gridHTML;
    stop_timer();
    cancelAllAnimationFrames();
}

function observeSolution(grid, chars, colors, region_map, move_history, i){
    if (i < move_history.length){
        window.requestAnimationFrame( () => {
            if (i == 0){
                showGrid(grid, chars, colors, region_map);
            }
            row = move_history[i][0][0]
            col = move_history[i][0][1]
            val = move_history[i][1]
            if (val == 0){
                document.getElementById(((row * grid[row].length)+col+1)).innerHTML = '';
            } else {
                document.getElementById(((row * grid[row].length)+col+1)).innerHTML = val;
            }
            sleepFor(200);
            observeSolution(grid, chars, colors, region_map, move_history, i+1);
        } );
    }
}

function sleepFor(sleepDuration){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* Do nothing */ }
}

function cancelAllAnimationFrames(){
   var id = window.requestAnimationFrame(function(){});
   while(id--){
     window.cancelAnimationFrame(id);
   }
}
