#!/usr/bin/env python3

import cgi, os, urllib
import cgitb
cgitb.enable()
import tag

xml = tag.maker()

head = xml.head()
header_tags = (xml.title('ConWorld'),)
default_tags = (xml.link(rel='stylesheet', type='text/css', href='stylesheet.css'),)
def with_default_tags(others):
    tags = list(default_tags)
    tags += others
    return tags

br = xml.br()
shitty_globe = xml.img(src='globe.gif')
site_title = xml.h1((shitty_globe, xml.u('Welcome to ConWorld'), shitty_globe))

# ================================================================ For printing different sections
def print_section_head(tag_set=default_tags):
    tags = list(tag_set)
    tags += header_tags
    head.print_tag(tag_set)

def write_status(code, exitparams=(False, 0)):
    print('Status: ' + code)
    if exitparams and exitparams[0]:
        end_headers()
        exit(exitparams[1] if len(exitparams) > 1 else 0)

def print_header():
    # THE TITLE
    site_title.print_tag()

    # THE NAVBAR
    br.print_tag()
    print('<h2>')
    print('<a href="index.py">Home</a>')
    print('<a href="about.py">About</a>')
    print('<a href="map.py">Map</a>')
    print('<a href="uh.py">and</a>')
    print('<a href="uh.py">some</a>')
    print('<a href="uh.py">more</a>')
    print('<a href="uh.py">links!</a>')
    print('</h2>')

def print_content():
    print('Fool, this ain\'t a page!')

def print_footer():
    br.print_tag()
    br.print_tag()
    print('<footer>')
    print('&copy; 2014.')
    print('</footer>')

# ================================================================ Utility functions
def print_shitty_globe():
    print('<img src="globe.gif" />')

# end_headers with one extra newline
end_headers = print

# ================================================================ The page starts getting printed
def write_page(content_printer, extra_header_tags=default_tags):
    print('Content-type: text/html')
    end_headers()
    print('<html>')
    print_section_head(extra_header_tags)
    print('<body>')
    print('<center>')

    print_header()
    content_printer()
    print_footer()

    print('</center>')
    print('</body></html>')

if __name__ == '__main__':
    write_page(print_content)
