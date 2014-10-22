#!/usr/bin/env python3

import index
import tag

xml = tag.maker()

maphtml = xml.div(xml.parsefile('map/map.html'), id="map.html")

def print_content():
    maphtml.print_tag()

if __name__ == '__main__':
    index.main(print_content)
