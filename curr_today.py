#!/usr/bin/env python3

import json
import sys
import urllib.request
import urllib.error

from decimal import *


def get_data(url):
    try:
        data = json.loads(urllib.request.urlopen("http://{}/day".format(url)).read())
        return data
    except urllib.error.HTTPError as ue:
        sys.exit(ue.msg)
    except json.decoder.JSONDecodeError as je:
        sys.exit(je.msg)
    except urllib.error.URLError as uue:
        sys.exit(uue.args)


if __name__ == "__main__":

    url = "localhost:8000"
    if len(sys.argv) >= 2:
        url = sys.argv[1]

    data = get_data(url)
    for line in data:
        if len(line) != 2:
            sys.exit("Wrong server responce")
        print("{}: {:10.4f}".format(line[0], line[1]))

