var config = {uri_get       : "cgi-bin/get.py",
              uri_separator : '/',
              uri_all_news  : "content/all-news.xml",
              uri_rss_image : "images/feed_icon.svg"
             };

function init_config () {
    config.uri_get = document.URL       + config.uri_separator + config.uri_get + '?value=';
    console.log("config.uri_get : "     + config.uri_get);
    config.uri_all_news = document.URL  + config.uri_all_news;
    console.log("config.uri_get : "     + config.uri_all_news);
    config.uri_rss_image = document.URL + config.uri_rss_image;
    console.log("config.uri_get : "     + config.uri_rss_image);
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
        "<li>Categories<ul>"     +
        categories           +
        "</ul></li><li>"          + 
        "<a href=\""         +  config.uri_all_news + "\"><image src=\"" +
        config.uri_rss_image + "\" height=\"16\"></image> RSS Feed</a></li></ul>";
    console.log(nav_element.innerHTML);
}

function initialize() {
    init_config();
    fill_navbar();
    show_content("recent_news");
}

