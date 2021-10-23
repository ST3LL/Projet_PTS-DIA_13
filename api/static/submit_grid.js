function submit_sudoku() {
    url = 'submit?sudoku='
    var emptyCellCount = 0;
    var cells = document.querySelectorAll('[contenteditable]');
    var i;
    for (i = 0; i < cells.length; i++) {
        if (cells[i].textContent == "") {
            url = url + '0';
            emptyCellCount = emptyCellCount + 1;
        }
        else{
            if (isNaN(cells[i].textContent) || cells[i].textContent < 1 || cells[i].textContent > 10) {
                alert("Input not valid");
                return;
            }
            url = url + cells[i].textContent;
        }
    }
    if (emptyCellCount > 64)
        alert("Please enter digits in all empty cases")
    else
        window.open (url,'_self',false);
}