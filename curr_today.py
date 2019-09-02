#!/usr/bin/env python3

import json
import sys
import urllib.request
import urllib.error



def usage():
    sys.exit("{} http://<address>:<port>".format(sys.argv[0]))


def get_data(url):
    try:
        data = json.loads(urllib.request.urlopen("{}/day".format(url)).read())
        return data
    except urllib.error.HTTPError as ue:
        sys.exit(ue.msg)
    except json.decoder.JSONDecodeError as je:
        sys.exit(je.msg)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()

    data = get_data(sys.argv[1])
    for line in data:
        if len(line) != 2:
            sys.exit("Wrong server responce")
        print("{}: {}".format(line[0], line[1]))