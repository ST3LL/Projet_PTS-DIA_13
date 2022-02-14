function str_list(list, is_matrice){
    list_str = '['
    list.forEach(function(c) {
        if (is_matrice){
            list_str += str_list(c, false) + ", "
        } else {
            list_str += "'" + c + "', "
        }
    });
    list_str = list_str.substring(0, list_str.length - 2) + ']'
    return list_str
}