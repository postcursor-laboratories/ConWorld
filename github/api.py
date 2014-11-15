API_URL = "https://api.github.com"

def get_url(frag):
    if frag[0] == '/':
        # fragment starts with /
        if API_URL[-1] == '/':
            # API_URL ends with it and we don't want //
            frag = frag[1:]
        else:
            # okay to pass
            pass
    else:
        # fragment does not start with /
        if API_URL[-1] == '/':
            # API_URL does, it will make /
            pass
        else:
            # there will not be a slash, add one
            frag = '/' + frag
    return API_URL + frag

with open('/home/kenzie/conworld-token') as tokenfile:
    token = tokenfile.read()

__all__ = ["get_url", "token"]
