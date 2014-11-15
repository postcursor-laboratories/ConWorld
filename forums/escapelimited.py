#!/usr/bin/env python3
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # top-level py
import conlib
import re
import requests
import cgi
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment
from http.client import OK, BAD_REQUEST

mdurl = 'https://api.github.com/markdown'
markdownheaders = {'Accept': 'application/vnd.github.v3+json'}

def github_markdown(unsafe):
    unsafe = cgi.escape(unsafe) # no HTML
    postdata = {'text': unsafe, 'mode': 'markdown'}
    response = requests.post(mdurl, json=postdata, headers=markdownheaders)
    return response.text

inputkey = 'input'
if __name__ == "__main__":
    form = cgi.FieldStorage()
    code = OK
    data = ''
    input_ = ''
    if not inputkey in form:
        input_ = form[inputkey]
        if not input_:
            code = BAD_REQUEST
            data = 'no data transmitted'
    data = github_markdown(input_)
    conlib.write_status(code)
    print('Content-type: text/plain')
    conlib.end_headers()
    if not data:
      print('no data .....?')
      sys.exit(0)
    print('yes, there is actually data')
    print(data)
