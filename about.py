#!/usr/bin/env python3

import conlib
import tag

xml = tag.maker()

def generate_content():
    link = 'http://slatestarcodex.com/2013/04/15/things-i-learned-by-spending-five-thousand-years-in-an-alternate-universe'
    text1 = (tag.TextTag('ConWorld is a game based on '), xml.a(href=link, content='this random blog post.'))
    text2 = tag.TextTag('Live in fear and appreciate the fine majesty of this beautious concoction.')
    return xml.p((text1, xml.br(), text2))

content = generate_content()

if __name__ == '__main__':
    conlib.write_page(content.print_tag)
