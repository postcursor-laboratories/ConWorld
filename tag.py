"""

XML tags made Pythonic.
"""
import collections
import bs4

class Tag:
    @staticmethod
    def __transform(x):
        if type(x) is str:
            pass
        elif isinstance(x, Tag):
            x = x.get_tag()
        elif isinstance(x, collections.Sequence):
            x = ''.join(str(Tag.__transform(o)) for o in x)
        return x
    def __init__(self, name, contents='', **kwargs):
        self.tag_name = name
        self.content = contents
        self.attrs = kwargs
    def __repr__(self):
        return self.get_tag()
    def get_tag(self):
        contents = Tag.__transform(self.content)
        attrstr = ' '.join(['{}={}'.format(x[0], x[1]) for x in self.attrs.items()])
        name_attrs = self.tag_name
        if attrstr:
            name_attrs += ' ' + attrstr
        tag = '<{}>{}</{}>'.format(name_attrs, contents, self.tag_name)
        return tag
    def print_tag(self):
        print(self.get_tag())
class TextTag(Tag):
    def __init__(self, text):
        super().__init__(None, text)
    def get_tag(self):
        return self.content

def maketag(name, content='', **kwargs):
    if name:
        return Tag(name, content, **kwargs)
    else:
        return TextTag(content)
def recursiveparse(node):
    tags = []
    if hasattr(node, 'children'):
        for child in node.children:
            tags += recursiveparse(child)
        if not isinstance(node, bs4.BeautifulSoup):
            tags = [maketag(node.name, content=tags)]
    else:
        tags.append(TextTag(str(node)))
    return tags

class TagMaker:
    def __init__(self):
        self.cache = {}
    def __getattr__(self, name):
        cache = self.cache
        if not name in cache:
            def make(content='', **kwargs):
                return maketag(name, content, **kwargs)
            cache[name] = make
        return cache[name]
    def parse(self, string):
        soup = bs4.BeautifulSoup(string)
        tag = recursiveparse(soup)
        return tag
    def parsefile(self, f):
        with open(f) as fd:
            return self.parse(fd.read())

makerInstance = TagMaker()
def maker():
    return makerInstance

__all__ = ["Tag", "maker"]