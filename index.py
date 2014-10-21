#!/usr/bin/env python3

import cgi, os, urllib
import cgitb
cgitb.enable()

# ================================================================ For printing different sections
def print_section_head():
    print('<head>')
    print('<title>ConWorld</title>')
    print('<link rel="stylesheet" type="text/css" href="stylesheet.css">')
    print('</head>')

def print_header():
    # THE TITLE
    print('<h1>')
    print_shitty_globe()
    print('<u>Welcome to ConWorld!</u>')
    print_shitty_globe()
    print('</h1>')

    # THE NAVBAR
    print('<br />')    
    print('<h2>')
    print('<a href="index.py">Home</a>')
    print('<a href="about.py">About</a>')
    print('<a href="map_playground.py">maptest</a>')
    print('<a href="uh.py">and</a>')
    print('<a href="uh.py">some</a>')
    print('<a href="uh.py">more</a>')
    print('<a href="uh.py">links!</a>')
    print('</h2>')

def print_content():
    print('<table border=4><tr><th>')
    #print('<h3><i><u><b>content approaching at rapid speeds!!</b></u></i></h3>')
    print('<img src="CONTENT.gif" />')
    print('<br />')
    print_shitty_globe()
    print('</th></tr></table>')    

def print_footer():
    print('<br />')
    print('<br />')
    print('<footer>')
    print('&copy; 2014.')
    print('</footer>')

# ================================================================ Utility functions
def print_shitty_globe():
    print('<img src="globe.gif" />')

# ================================================================ The page starts getting printed
def main(content_printer):
    print('Content-type: text/html')
    print()
    print('<html>')    
    print_section_head()
    print('<body>')
    print('<center>')

    print_header()
    content_printer()
    print_footer()

    print('</center>')
    print('</body></html>')

if __name__ == '__main__':
    main(print_content)
