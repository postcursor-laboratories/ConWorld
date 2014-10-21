#!/usr/bin/env python3

import index

def print_content():
    print("""
<style type="text/css">
	.draggable{
		position:relative;
		cursor: move;
	}

	#map{
		width: 1000px;
		height: 700px;
		background-color: darkgrey;
	}
</style>
<script src="mapping.js"></script>
""")

    print('<table border=4><tr><th style="overflow: hidden;">')
    print('<div id="map">')
    print("<img id='mapImage' src='someRandomMap.jpg' class='draggable' style='top:-500px;left:-500px;zoom=1' />")
    #print("<img src='http://3.bp.blogspot.com/--Qn8gNCWlUc/UVhKBl5o5aI/AAAAAAAACYI/wMLgckCYQIs/s1600/Screen+Shot+2013-03-31+at+12.59.10+AM.png' class='draggable' />")
    print('</div>')
    print('</th></tr></table>')

if __name__ == '__main__':
    index.main(print_content)
