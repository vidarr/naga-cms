var config = {
    id_div_main_menu : "div_main_menu"
};

var div_menu_state = 0;
var old_nav_height = "12em";

function show_dynamic_menu() {
    var div_menu = document.getElementById("div_main_menu");
    var nav = document.getElementsByTagName("nav")[0]; 
    var article = document.getElementsByTagName("article")[0]; 
    console.log(div_menu);
    console.log(div_menu.innerHTML);
    div_menu.style.display = "block";
    article.style.display = "none";
    nav.style.height;
    console.log(nav.style);
    nav.style.height = "auto";
}

function hide_dynamic_menu() {
    var div_menu = document.getElementById("div_main_menu");
    var nav = document.getElementsByTagName("nav")[0]; 
    var article = document.getElementsByTagName("article")[0]; 
    console.log(div_menu);
    console.log(div_menu.innerHTML);
    div_menu.style.display = "none";
    article.style.display = "inline-block";
    console.log(nav.style);
    nav.style.height = "12em";
}
    
function toggle_dynamic_menu() {
    if(div_menu_state == 0) {
        show_dynamic_menu();
    } else {
        hide_dynamic_menu();
    }
    div_menu_state = 1 - div_menu_state;
}

