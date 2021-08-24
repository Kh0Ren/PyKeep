import sys
import argparse
import requests


def createparser():
    par = argparse.ArgumentParser()
    par.add_argument('-s', '--server', help='server\'s URL')

    subpars = par.add_subparsers(dest='command', help='commands for interacting with keeps')

    viewpar = subpars.add_parser('view', help='View names ot notes of categories', description='View keep or keeps')
    viewpar.add_argument('--category', help='View notes of specific category')
    viewpar.add_argument('--categories', action='store_const', const=1, help='View names of categories')
    viewpar.add_argument('--noteid', type=int, help='View the note by id. Used with --category')

    addcatpar = subpars.add_parser('addcat', help='Add category', description='Add category')
    addcatpar.add_argument('--category', help='New category of notes')

    addnotepar = subpars.add_parser('addnote', help='Add note', description='Add note')
    addnotepar.add_argument('--note', help='Text of note. Used with --category')
    addnotepar.add_argument('--catname', help='Name of existing category')

    delcatpar = subpars.add_parser('delcat', help='Delete category', description='Delete category')
    delcatpar.add_argument('--name', help='name of category')

    delnotepar = subpars.add_parser('delnote', help='Delete note', description='Delete note')
    delnotepar.add_argument('--catname', help='Name of category')
    delnotepar.add_argument('--noteid', help='Note\'s id')

    changecatpar = subpars.add_parser('changecat', help='Change name of category',
                                      description='Change name of category')
    changecatpar.add_argument('--name', help='Name of category')
    changecatpar.add_argument('--newname', help='New name of category')

    changenotepar = subpars.add_parser('changenote', help='Change text of note',
                                       description='Change text of note')
    changenotepar.add_argument('--catname', help='Name of category')
    changenotepar.add_argument('--noteid', help='Note\'s id')
    changenotepar.add_argument('--text', help='New text of note. Used with --noteid and --catname')

    return par


if __name__ == '__main__':
    parser = createparser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.server:

        if namespace.command == 'view':
            if namespace.categories and namespace.category is None:
                r = requests.get('{}/categories'.format(namespace.server))
                print(r.text)

            elif namespace.category and namespace.categories is None:
                if namespace.noteid:
                    r = requests.get('{}/categories/{}/{}'.format(namespace.server,
                                                                  namespace.category, namespace.noteid))
                    print(r.text)
                else:
                    r = requests.get('{}/categories/{}'.format(namespace.server, namespace.category))
                    print(r.text)

            elif namespace.categories is not None and namespace.category is not None:
                print('Error: use only one of this arguments')

            else:
                print('Enter view -h to see the arguments')

        elif namespace.command == 'addcat':
            if namespace.category:
                r = requests.post('{}/categories?name={}'.format(namespace.server, namespace.category))
                print(r.text)
            else:
                print('Enter add -h to see the arguments')

        elif namespace.command == 'addnote':
            if namespace.note and namespace.catname:
                r = requests.post('{}/categories/{}?text={}'.format(namespace.server,
                                                                    namespace.catname, namespace.note))
                print(r.text)
            else:
                print('Error: argument --note must be used with --category')

        elif namespace.command == 'delcat':
            if namespace.name:
                r = requests.delete('{}/categories/{}'.format(namespace.server, namespace.name))
                print(r.text)
            else:
                print('Enter delete -h to see the arguments')

        elif namespace.command == 'delnote':
            if namespace.noteid and namespace.catname:
                r = requests.delete('{}/categories/{}/{}'.format(namespace.server,
                                                                 namespace.catname, namespace.noteid))
                print(r.text)
            else:
                print('Error: arguments --noteid and --catname required to delete the note.'
                      ' Enter -h for help')

        elif namespace.command == 'changecat':
            if namespace.name and namespace.newname:
                r = requests.put('{}/categories/{}?name={}'.format(namespace.server,
                                                                   namespace.name, namespace.newname))
                print(r.text)
            else:
                print('Error: arguments --name and --newname required to change the name of category.'
                      ' Enter -h for help')

        elif namespace.command == 'changenote':
            if namespace.catname and namespace.noteid and namespace.text:
                r = requests.put('{}/categories/{}/{}?text={}'.format(namespace.server,
                                                                      namespace.catname, namespace.noteid,
                                                                      namespace.text))
                print(r.text)
            else:
                print('Error: arguments --catname, --noteid and --text'
                      ' required to change the text of note')

        else:
            parser.print_help()

    else:
        parser.print_help()
