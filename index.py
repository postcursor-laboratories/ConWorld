#!/usr/bin/env python3
import conlib

def print_content():
    print('<table border=4><tr><th>')
    #print('<h3><i><u><b>content approaching at rapid speeds!!</b></u></i></h3>')
    print('<img src="CONTENT.gif" />')
    conlib.br.print_tag()
    conlib.print_shitty_globe()
    print('</th></tr></table>')

if __name__ == '__main__':
    conlib.write_page(print_content)
