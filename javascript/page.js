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

function show_content (key) {
    content = get_from_page(key);
    var elements = document.getElementsByTagName("article");
    console.log(elements);
    var article_element = elements[0];
    console.log(article_element.innerHTML);
    article_element.innerHTML = content;
}

function fill_navbar() {
    categories = get_from_page("categories");
    var elements = document.getElementsByTagName("nav");
    console.log(elements);
    var nav_element = elements[0];
    console.log(nav_element.innerHTML);
    nav_element.innerHTML =
        "<ul><li onclick='show_content(\"all_news\")'>All News</li>" +
        "<li>Categories" +
        categories         +
        "</li></ul>";
}

function initialize() {
    init_config();
    fill_navbar();
    show_content("recent_news");
}

