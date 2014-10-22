#!/usr/bin/env python3

import index
import tag

xml = tag.maker()
text = xml.b("my bad formatting brings all the browsers to the yard")
one23 = xml.ul((xml.li('one'), xml.li('two'), xml.li('three')))

def print_content():
    text.print_tag()
    one23.print_tag()

if __name__ == '__main__':
    index.main(print_content)
