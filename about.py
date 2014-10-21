#!/usr/bin/env python3

import index

def print_content():
    print("""<p>
ConWorld is a game based on <a href="http://slatestarcodex.com/2013/04/15/things-i-learned-by-spending-five-thousand-years-in-an-alternate-universe/">this random blog post.</a>
<br />
Live in fear and appreciate the fine majesty of this beautious concoction.
</p>
""")

if __name__ == '__main__':
    index.main(print_content)
