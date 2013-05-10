==============================
django-lifestream
==============================

django-lifestream is a lifestream application for django. It allows
you to create a lifestream on your site easily.

A lifestream is a collection of items that are pulled from the
internet via feeds (RSS + Atom). Typically these include your
blog feed, your flickr feed, your delicious feed etc.

HTML Sanitization
------------------------------

django-lifestream will sanitize the data coming from these feeds
so that you can show html content from these feeds without worrying
about the html containing nasty stuff that will expose your users to
harm like some malicious javascript or a css hack 
(see: http://diveintomark.org/archives/2003/06/12/how_to_consume_rss_safely).
It also helps maintain the layout of your site by fixing unclosed html tags
and sanitizing invalid characters like <, >, ", '
and replacing them with the appropriate entities.

You can choose which tags and attributes that django-lifestream will
allow by setting LIFESTREAM_VALID_TAGS in your site's settings.py.
LIFESTREAM_VALID_TAGS is a dictionary whose key is the html tag name
and the value is a list of attributes that are allowed for that tag.
An empty list specifies that all attributes will be stripped from the
tag. A value of None will specify that all attributes are allowed.
The dictionary only contains valid tags. Tags not present in the
dictionary will be stripped from html. The default setting can be
seen in the VALID_TAGS dictionary in lifestream/util/__init__.py.

Templates
-----------------------------
django-lifestream includes functionality for rendering lifestream items
using different templates. This is done on a per feed domain basis.
Each feed has a domain property which is populated automatically
when you register the feed but can be changed later.

To use different templates per domain you create two templates, one
for the lifestream list page and one for the item's detail page.
You place the template in the lifestream/sites/ directory in your
templates include path. The name of the list page's
template is the name of the domain with '.' characters replaced with
'-' characters and and html extension. So flickr.com's feed would have
a template named 'flickr-com.html'. The detail page's template has
the same name but is given a '_detail' suffix
(i.e. flickr-com_detail.html).

The item is rendered in templates using the 'render_item' template
tag. You might have a template like so::

    {% load lifestream_tags %}

    {% for object in object_list %}
    <div class="item">
    {% render_item object %}
    </div>
    {% endfor %}


Views
-----------------------------
django-lifestream includes some basic views for displaying the
lifestream, displaying individual items, showing item's by domain, and
rendering a RSS feed for the lifestream.

The standard lifestream views use the django's list based generic
views so templates that work with generic views should work with
django-lifestream. The default views are paginated using
a default page size of 20 but that can be overridden by setting
the LIFESTREAM_DEFAULT_PAGINATION setting in your settings.py.

Tags
-----------------------------
django-lifestream includes support for automatically importing
tags from feeds and saving them using dango-tagging. This support
is optional and is only turned on only if you include 'tagging' in your
INSTALLED_APPS.

Plugins
-----------------------------
django-lifestream includes support for plugins which can massage
feed content before saving it in the database. This can include things
like removing tags that you don't want to show on your site, filtering
feed content to remove content with profanity, or massaging the text
in the feed content. A few reference plugins have been included
for commonly used sites. These may or may not work well with the
feeds you are using and it's recommended that you write your own.

Plugins can be registered with the application by adding them to the
PLUGINS list in your site's settings.py. The PLUGINS is a two tuple
which contains the module path to the plugin class and the plugin name.

Caching
-----------------------------
django-lifestream will use feedcache if it can be imported otherwise
it will use feedparser normally. Feed data will be cached using
django's cache backend.

Updating Your Lifestream
-----------------------------
django-lifestream includes a django command, update_feeds, for
updating all feeds which can be run using manage.py. This can be
run as a cron job that will update your lifestream periodically. It
can be run simply by invoking manage.py with the update_feeds command.

::

    python manage.py update_feeds

This will import all new items from all feeds that are specified as
fetchable.
