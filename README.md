# naga-cms

## What is it?

'''naga-cms''' is a web based content-management-system.
It has been written in Python 3 and facilitates the [wsgi](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface).

It currently powers the larger part of [my personal website](https://ubeer.org)

*Beware*: I created this CMS mainly for my own use, thus it might be a bit edgy to use...

## Installation & Usage

'''naga''' has been developped to be used with the Apache web server.
The WSGI module needs to be installed and enabled. 

Use the  release.sh` script to build a tarball suited for delivery.
It requires one command line argument, the target place where to move the tarball to.
Once you got the tarball, unzip it into the WSGi directory of Apache.

Once extracted, have a look at `setup.cfg` and adapt the variables in there according to your needs.

Finally, invoke `setup.sh`. This will set up file permissions etc. properly.

Once running, it should be suffient to use your favourite browser to navigate to `your_server/path/to/wsgi_dir/index.html`.

If you want to modify content, you need to set up a user using the script `tools/adduser.py`.
Then navigate with your browser to `your_server/path/to/wsgi_dir/wsgi/login.py` (Yes, you have to navigate there by entering the
link, there is no link to that page on the web page).

Once logged in, new links appear on the web page, that allow you to change / add content.

The CMS uses its own markup language, that is described in `doc/README` .

Cheerio!
