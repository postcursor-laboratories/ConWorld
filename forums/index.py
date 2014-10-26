import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..')) # top-level py
import tag
import conlib

xml = tag.maker()

with open('index_contents.html') as f:
    contents = xml.parse(f.read())[0]
    print(contents)

with open('index_headtag.html') as f:
    headertags = xml.parse(f.read())
    print(headertags)

if __name__ == "__main__":
    conlib.write_page(contents.print_tag, conlib.with_default_tags(headertags))
