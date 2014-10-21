"""

XML tags made Pythonic.
"""
class Tag:
    def __init__(self, name, contents='', **kwargs):
        self.tag_name = name
        self.content = contents
        self.attrs = kwargs
    def print_tag(self):
        attrstr = ' '.join(['{}={}'.format(x[0], x[1]) for x in self.attrs.iterkeys()])
        tag = '<{} {}>{}</{}>'.format(self.tag_name, attrstr, self.content, self.tag_name)
        print(tag)

class TagMaker:
    def __init__(self):
        self.cache = {}
    def __getattr__(self, name):
        if not name in cache:
            def make(content='', **kwargs):
                return Tag(name, content, **kwargs)
            cache[name] = make
        return cache[name]

makerInstance = TagMaker()
def maker():
    return makerInstance

__all__ = ["Tag", "maker"]
