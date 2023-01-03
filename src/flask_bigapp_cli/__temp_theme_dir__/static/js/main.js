function showEle(element_id, display_as = "block") {
    let div = document.getElementById(element_id);
    div.style.display = display_as;
}

function hideEle(element_id) {
    let div = document.getElementById(element_id);
    div.style.display = "none";
}