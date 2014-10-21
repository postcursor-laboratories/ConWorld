#!/usr/bin/env python3

import index

def print_content():
    print("""Content-type: text/plain

<b>my bad formatting brings all the browsers to the yard
<ul><li>one<li>two<li>three""")

if __name__ == '__main__':
    index.main(print_content)
