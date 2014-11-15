#!/usr/bin/env python3
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # top-level py
import conlib
import requests
import datetime
from github.api import get_url, auth
conlib.rewrite_relatives(levels=1)

def get_raw_rate_json(request_auth=auth):
    req = requests.get(get_url('/rate_limit'), auth=request_auth)
    req.raise_for_status()
    json = req.json()
    return json
def get_rate_data(location='core', **kwargs):
    data = get_raw_rate_json(**kwargs)
    rldata = data['resources'][location]
    return rldata
mla = '%d %B %Y @ %I:%M:%S %p'
def readable_date(millis_since_epoch):
    # my english teacher wants this to be mla formatted
    return datetime.datetime.fromtimestamp(millis_since_epoch).strftime(mla)
def write_rate_limit():
    corerate = get_rate_data()
    print('Core rate data:', "{}/{}, resets on {}".format(corerate['remaining'],
                                                          corerate['limit'],
                                                          readable_date(corerate['reset'])))

if __name__ == "__main__":
    conlib.write_page(write_rate_limit)
