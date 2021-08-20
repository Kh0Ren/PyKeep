import sys
import argparse
import requests
import json


def createparser():
    par = argparse.ArgumentParser()
    par.add_argument('-s', '--server', required=True)
    subpars = par.add_subparsers(dest='command')
    compar = subpars.add_parser('command')
    compar.add_argument('--keep', type=int)
    compar.add_argument('--keeps', action='store_const', const=1)
    compar.add_argument('--add')
    compar.add_argument('--change', type=int)
    compar.add_argument('--delete', type=int)

    return par


parser = createparser()
namespace = parser.parse_args(sys.argv[1:])

if namespace.server:
    if namespace.command == 'command':
        if namespace.keep:
            r = requests.get('{}/keeps/{}'.format(namespace.server, namespace.keep))
            print(r.text)

        if namespace.keeps:
            r = requests.get('{}/keeps'.format(namespace.server))
            print(r.text)

        if namespace.add:
            r = requests.post('{}/keeps?keep={}'.format(namespace.server, namespace.add))
            print(r.text)

        if namespace.delete:
            r = requests.delete('{}/keeps/{}'.format(namespace.server, namespace.delete))
            print(r.text)


