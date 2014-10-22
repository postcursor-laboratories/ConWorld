#!/usr/bin/env python3

import index
import tag

maphtml = tag.maker().parsefile('map/map.html')[0]

def print_content():
    maphtml.print_tag()

if __name__ == '__main__':
    index.main(print_content)
