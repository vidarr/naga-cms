var config = {uri_get : "cgi-bin/get.py",
              uri_separator : '/'
             };

function init_config () {
    config.uri_get = document.URL + config.uri_separator + config.uri_get + '?value=';
    console.log("config.uri_get : " + config.uri_get);
}

function get_from_page(value) {
    var uri = config.uri_get + value;
    var request = XMLHttpRequest();
    request.open("GET", uri, false);
    request.send(null);
    if(request.status != 200) throw new Error(request.statusText);
    var type =request.getResponseHeader("Content-Type");
    if(! type.match(/^text/))
        throw new Error("Expected repsonse with Content-Type: Text");
    console.log("get_from_page(): " + request.responseText);
    return request.responseText;
}

function fill_navbar() {
    categories = get_from_page("categories");
    var elements = document.getElementsByTagName("nav");
    console.log(elements);
    var nav_element = elements[0];
    console.log(nav_element.innerHTML);
    nav_element.innerHTML =
        "<item>Categories" +
        categories         +
        "</item>";
}

    
function initialize() {
    init_config();
    fill_navbar();
}

