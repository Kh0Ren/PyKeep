import sys
import argparse
import requests


def createparser():
    par = argparse.ArgumentParser()
    par.add_argument('-s', '--server')

    subpars = par.add_subparsers(dest='command')

    viewpar = subpars.add_parser('view')
    viewpar.add_argument('--keep', type=int)
    viewpar.add_argument('--keeps', action='store_const', const=1)

    addpar = subpars.add_parser('add')
    addpar.add_argument('--keep')

    delpar = subpars.add_parser('delete')
    delpar.add_argument('--keep', type=int)

    changepar = subpars.add_parser('change')
    changepar.add_argument('--keep', type=int)
    changepar.add_argument('--note')

    return par


parser = createparser()
namespace = parser.parse_args(sys.argv[1:])

if namespace.server:

    if namespace.command == 'view':
        if namespace.keeps:
            r = requests.get('{}/keeps'.format(namespace.server))
            print(r.text)
        else:
            print('Error: required argument --keeps')

        if namespace.keep:
            r = requests.get('{}/keeps/{}'.format(namespace.server, namespace.keep))
            print(r.text)
        else:
            print('Error: required argument --keep')

    if namespace.command == 'add':
        if namespace.keep:
            r = requests.post('{}/keeps?keep={}'.format(namespace.server, namespace.keep))
            print(r.text)
        else:
            print('Error: required argument --keep')

    if namespace.command == 'delete':
        if namespace.keep:
            r = requests.delete('{}/keeps/{}'.format(namespace.server, namespace.keep))
            print(r.text)
        else:
            print('Error: required argument --keep')

    if namespace.command == 'change':
        if namespace.keep and namespace.note:
            r = requests.put('{}/keeps/{}?keep={}'.format(namespace.server, namespace.keep, namespace.note))
            print(r.text)
        else:
            print('Error: required all arguments of command change')

    else:
        print('Error: enter command')


else:
    print('Error: required argument -s/--server')
