#!/usr/bin/env python3

import index

def print_content():
    print("""
<style type="text/css">
	.draggable{
		position:relative;
		cursor: move;
	}
</style>
<script src="mapping.js" />
""")                            # WHY CAN'T I INCLUDE THIS SCRIPT AARHGH

    print('<table border=4><tr><th>')
    #print("<img src='someRandomMap.jpg' class='draggable' />")
    print("<img src='http://3.bp.blogspot.com/--Qn8gNCWlUc/UVhKBl5o5aI/AAAAAAAACYI/wMLgckCYQIs/s1600/Screen+Shot+2013-03-31+at+12.59.10+AM.png' />")
    print('</th></tr></table>')

if __name__ == '__main__':
    index.main(print_content)
