import sys
import argparse
import requests


def createparser():
    par = argparse.ArgumentParser()
    par.add_argument('-s', '--server', help='server\'s URL')

    subpars = par.add_subparsers(dest='command', help='commands for interacting with keeps')

    viewpar = subpars.add_parser('view', help='View keep or keeps', description='View keep or keeps')
    viewpar.add_argument('--id', type=int, help='view the keep by id')
    viewpar.add_argument('--keeps', action='store_const', const=1, help='view all keeps')

    addpar = subpars.add_parser('add', help='add keep', description='add keep')
    addpar.add_argument('--keep', help='new keep')

    delpar = subpars.add_parser('delete', help='delete keep', description='delete keep')
    delpar.add_argument('--id', type=int, help='keep\'s id')

    changepar = subpars.add_parser('change', help='change keep', description='change keep')
    changepar.add_argument('--id', type=int, help='keep\'s id')
    changepar.add_argument('--note', help='new text of keep')

    return par


parser = createparser()
namespace = parser.parse_args(sys.argv[1:])

if namespace.server:

    if namespace.command == 'view':
        if namespace.keeps:
            r = requests.get('{}/keeps'.format(namespace.server))
            print(r.text)

        elif namespace.id:
            r = requests.get('{}/keeps/{}'.format(namespace.server, namespace.id))
            print(r.text)

        else:
            print('Enter view -h to see the arguments')

    elif namespace.command == 'add':
        if namespace.keep:
            r = requests.post('{}/keeps?keep={}'.format(namespace.server, namespace.keep))
            print(r.text)

        else:
            print('Enter add -h to see the arguments')

    elif namespace.command == 'delete':
        if namespace.id:
            r = requests.delete('{}/keeps/{}'.format(namespace.server, namespace.id))
            print(r.text)

        else:
            print('Enter delete -h to see the arguments')

    elif namespace.command == 'change':
        if namespace.id and namespace.note:
            r = requests.put('{}/keeps/{}?keep={}'.format(namespace.server, namespace.id, namespace.note))
            print(r.text)

        else:
            print('Enter view -h to see the arguments')

    else:
        parser.print_help()


else:
    parser.print_help()
