#!/usr/bin/env python3

import cgi
import os
import sys

#import cgitb
#cgitb.enable()

if __name__ == '__main__':
    form = cgi.FieldStorage()

    try:
        tile = form['n'].value + '.png'
    except KeyError:
        exit(1)

    tile = "tiles/"+tile

    if not os.path.isfile(tile):
        tile = "tiles/unexplored.png"

    # Redirect
    print("Location: " + tile)
    print("Content-Type: text/html")
    print()

    # idk, just in case? The Location header above works for chrome, but idk about all browsers, so..
    print("<html><head>")
    print("<script>window.location.href={}</script>".format(tile))
    print("<meta http-equiv='refresh' content='0; url={}' />".format(tile))
    print("</head></html>")
