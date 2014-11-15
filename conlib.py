#!/usr/bin/env python3

import cgi, os, urllib, sys, re
import tag

xml = tag.maker()

head = xml.head()
head_tags = (xml.title('ConWorld'),)
default_tags = (xml.link(rel='stylesheet', type='text/css', href='stylesheet.css'),)
def with_default_tags(others):
    tags = list(default_tags)
    tags += others
    return tags

br = xml.br()
shitty_globe = xml.img(src='globe.gif')
site_title = xml.h1((shitty_globe, xml.u('Welcome to ConWorld'), shitty_globe))

links = xml.links([['index.py', 'Home'], ['about.py', 'About'], ['map.py', 'Map'], ['forums', 'Forums'],
                  ['uh.py', 'and'], ['uh.py', 'some'], ['uh.py', 'more'], ['uh.py', 'links!']])

# rewrite conlib so it works in different levels
levels_down = 0
notrelative = re.compile('^(?!(//)|(http://)||(https://)|)')
def rewrite_relatives(levels):
    global levels_down
    if levels > levels_down:
        levels -= levels_down
    elif levels < levels_down:
        # we are trying to back out
        # unsupport operation right now
        raise ValueError("{} < {}, cannot back out".format(levels, levels_down))
    prepend = '../' * levels
    def rewrite(tag):
        if tag.tag_name in ['img', 'script'] and notrelative.match(tag.attrs['src']) is None:
            # images and scripts
            tag.attrs['src'] = prepend + tag.attrs['src']
        elif tag.tag_name in ['link', 'a'] and notrelative.match(tag.attrs['href']) is None:
            # stylesheets and links
            tag.attrs['href'] = prepend + tag.attrs['href']
    [rewrite(tag) for tag in default_tags]
    rewrite(shitty_globe)
    [rewrite(tag) for tag in links]
    levels_down += levels
# ================================================================ For printing different sections
def print_section_head(tag_set=default_tags):
    tags = list(tag_set)
    tags += head_tags
    head.print_tag(tag_set)

def write_status(code, exitparams=(False, 0)):
    print('Status: ' + str(code))
    if exitparams and ((not hasattr(exitparams, '__getitem__')) or exitparams[0]):
        end_headers()
        sys.exit(exitparams[1] if hasattr(exitparams, '__len__') and len(exitparams) > 1 else 0)

def print_header():
    # THE TITLE
    site_title.print_tag()

    # THE NAVBAR
    br.print_tag()
    # special link conversion
    xml.h2(' '.join(str(l) for l in links)).print_tag()

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
    shitty_globe.print_tag()

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
