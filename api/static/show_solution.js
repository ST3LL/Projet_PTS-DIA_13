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

function observeSolution(grid, grid_solved, chars, colors, region_map, move_history, i, nb_values){
    if (i < move_history.length){
        time_tot = 30
        fps = 3
        n = move_history.length
        batch = Math.round(n/(fps*time_tot))+1
        if (i%batch == 0 || i == move_history.length - 1){
            window.requestAnimationFrame( () => {
                observeSolutionBis(grid, grid_solved, chars, colors, region_map, move_history, i, nb_values);
            } );
        } else {
            observeSolutionBis(grid, grid_solved, chars, colors, region_map, move_history, i, nb_values);
        }


    } else {
        submit_grid('sudoku_grid', grid_solved)
    }
}

function observeSolutionBis(grid, grid_solved, chars, colors, region_map, move_history, i, nb_values){
    if (i == 0){
        showGrid(grid, chars, colors, region_map);
        document.getElementById('move_label').innerHTML = 'Move statistics';
        document.getElementById('solution_label').innerHTML = 'Solution statistics';
    }
    row = move_history[i][0]
    col = move_history[i][1]
    val = move_history[i][2]
    actual_case = document.getElementById(((row * grid[row].length)+col+1)).innerHTML;
    if (grid_solved[row][col].toString() == actual_case){
        regress = true
    } else {
        regress = false
    }

    if (val == 0){
        document.getElementById(((row * grid[row].length)+col+1)).innerHTML = '';
    } else {
        document.getElementById(((row * grid[row].length)+col+1)).innerHTML = val;
    }
    document.getElementById('move_counter').innerHTML = i+1 + '/' + move_history.length;
    document.getElementById('move_percent').innerHTML = roundDecimal(((i+1) / move_history.length)*100, 4) + '%';
    sleepFor(3000/move_history.length);
    if (grid_solved[row][col] == val){
        nb_values += 1
    } else if (regress) {
        nb_values -= 1
    }
    document.getElementById('solution_counter').innerHTML = (nb_values) + '/' + (grid.length*grid[0].length);
    document.getElementById('solution_percent').innerHTML = roundDecimal(((nb_values) / (grid.length*grid[0].length))*100, 4) + '%';
    observeSolution(grid, grid_solved, chars, colors, region_map, move_history, i+1, nb_values);
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
    document.getElementById('move_label').innerHTML = '';
    document.getElementById('solution_label').innerHTML = '';
    document.getElementById('move_counter').innerHTML = '';
    document.getElementById('move_percent').innerHTML = '';
    document.getElementById('solution_counter').innerHTML = '';
    document.getElementById('solution_percent').innerHTML = '';
}

function roundDecimal(number, precision){
    var precision = precision || 2;
    var tmp = Math.pow(10, precision);
    return Math.round(number * tmp)/tmp;
}