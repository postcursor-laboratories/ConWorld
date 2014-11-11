#!/usr/bin/env python3
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # top-level py
import conlib
import re
from urlparse import urljoin
from bs4 import BeautifulSoup, Comment
from http.client import OK, BAD_REQUEST
codeset = 'img, b, i, em, strong, strike, p, header'.split(', ')

def limited_escape(string):
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = 'p em i strong b u a h1 h2 h3 pre br img'.split()
    validAttrs = 'href src width height'.split()
    urlAttrs = 'href src'.split() # Attributes which should have a URL
    soup = BeautifulSoup(string)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))

    return soup.renderContents().decode('utf8')
def glidus_glue_code(ggcodestr):
    glidus = '|'

inputkey = 'input'
if __name__ == "__main__":
    form = cgi.FormStorage()
    code = OK
    data = ''
    input_ = ''
    if not inputkey in form or not (input_ = form[inputkey]):
        code = BAD_REQUEST
        data = 'no data transmitted'
    data = limited_escape(input_)
    data = glidus_glue_code(data)
    conlib.write_status(code)
    print('Content-type: text/plain')
    conlib.end_headers()
    print(data)
