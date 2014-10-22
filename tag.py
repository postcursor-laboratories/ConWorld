"""

XML tags made Pythonic.
"""
import collections

class Tag:
    @staticmethod
    def __transform(x):
        if type(x) is str:
            pass
        elif type(x) is Tag:
            x = x.get_tag()
        elif isinstance(x, collections.Sequence):
            x = ''.join([Tag.__transform(o) for o in x])
        return x
    def __init__(self, name, contents='', **kwargs):
        self.tag_name = name
        self.content = contents
        self.attrs = kwargs
    def get_tag(self):
        contents = Tag.__transform(self.contents)
        attrstr = ' '.join(['{}={}'.format(x[0], x[1]) for x in self.attrs.iterkeys()])
        tag = '<{} {}>{}</{}>'.format(self.tag_name, attrstr, contents, self.tag_name)
        return tag
    def print_tag(self):
        print(self.get_tag())

class TagMaker:
    def __init__(self):
        self.cache = {}
    def __getattr__(self, name):
        cache = self.cache
        if not name in cache:
            def make(content='', **kwargs):
                return Tag(name, content, **kwargs)
            cache[name] = make
        return cache[name]

makerInstance = TagMaker()
def maker():
    return makerInstance

__all__ = ["Tag", "maker"]
