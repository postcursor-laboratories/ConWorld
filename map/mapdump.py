#!/usr/bin/env python3

# This generates a webpage that is a table of tiles, for easy looking at large expanses of tiles.

x0, x1 = -3, 3
y0, y1 = -3, 3

print("Content-Type: text/html")
print()

print("<html><body><p>Showing from x=[%d..%d], y=[%d..%d]</p>" % (x0, x1, y0, y1))

print("<table cellpadding=0 cellspacing=0>")

y = y0
while y < y1:
    print("<tr>")

    x = x0
    while x < x1:
        name = "tile_%d_%d" % (x, y)
        print("<td><img src='tiles/%s.png' title='%s' /></td>" % (name, name))
        x+=1

    print("</tr>")
    y+=1

print("</table></body></html>")
