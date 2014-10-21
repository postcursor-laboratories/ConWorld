#!/usr/bin/env python3

import index

def print_content():
    with open("map/map.html", "r") as fin:
        print(fin.read())

if __name__ == '__main__':
    index.main(print_content)
