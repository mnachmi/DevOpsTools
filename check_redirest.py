#!/usr/bin/env python

import sys
import requests
from urlparse import urlparse
from urlparse import urlunsplit


NOT_FOUND = ' [404 not found]'
SERVER_ERROR = ' [Server error]'
NO_REDIRECT = ' [No redirect]'


def check_for_redirects(url):
    try:
        s = ""
        r = requests.get(url, allow_redirects=False, timeout=20)
        if 200 <= r.status_code < 300:
            return url
        elif 300 <= r.status_code < 400:
            if r.headers['location'].startswith('/'):
                o = urlparse(url)
                s = urlunsplit((str(o.scheme), str(o.netloc), "", "", ""))
            return check_for_redirects(s + r.headers['location'])
        elif 400 <= r.status_code < 500:
            return str(url) + str(r.status_code) + NOT_FOUND
        else:
            return str(url) + str(r.status_code) + SERVER_ERROR
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'


def check_domains(urls):
    for url in urls:
        url_to_check = url if url.startswith('http') else "http://%s" % url
        # redirect_url = check_for_redirects(url_to_check)
        print "Processing...  " + url_to_check
        with open('output.txt', 'a') as f:
            f.write(check_for_redirects(url_to_check))
            f.write('\n')
            f.flush()

if __name__ == '__main__':
    of = open('output.txt', 'a')
    try:
        fname = sys.argv[1]
    except IndexError:
        fname = 'domains.txt'
    urls = (l.strip() for l in open(fname).readlines())
    check_domains(urls)
