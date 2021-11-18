function submit_sudoku() {
//    if ({{grid}} == {{solved_grid}}){
    if ('grid' == 'solved_grid'){
        document.getElementById("win").innerHTML = "Victoire !";
    }
    else {
        document.getElementById("win").innerHTML = "La grille n'est pas valide !";
    }
}
