#!/usr/bin/env python3
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..')) # top-level py
import re
import tag
import conlib

xml = tag.maker()

with open('index_contents.html') as f:
    contents = xml.parse(f.read())[0]

with open('index_headtag.html') as f:
    headertags = xml.parse(f.read())

# rewrite conlib so it works in forums
notrelative = re.compile('^(?!(//)|(http://)||(https://)|)')
def rewrite_for_forums(tag):
    if tag.tag_name in ['img', 'script'] and notrelative.match(tag.attrs['src']) is None:
        # images and scripts
        tag.attrs['src'] = '../' + tag.attrs['src']
    elif tag.tag_name in ['link', 'a'] and notrelative.match(tag.attrs['href']) is None:
        # stylesheets and links
        tag.attrs['href'] = '../' + tag.attrs['href']
[rewrite_for_forums(tag) for tag in conlib.default_tags]
rewrite_for_forums(conlib.shitty_globe)

if __name__ == "__main__":
    conlib.write_page(contents.print_tag, conlib.with_default_tags(headertags))
