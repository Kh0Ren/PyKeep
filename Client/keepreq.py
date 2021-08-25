import sys
import argparse
import requests


class NoteServerClient:
    def __init__(self, server):
        self.server = server

    def view_categories(self):
        r = requests.get('{}/categories'.format(self.server))
        return r.text

    def view_notes(self, catname):
        r = requests.get('{}/categories/{}'.format(self.server, catname))
        return r.text

    def view_note(self, catname, noteid):
        r = requests.get('{}/categories/{}/{}'.format(self.server,
                                                      catname, noteid))
        return r.text

    def add_category(self, name):
        r = requests.post('{}/categories?name={}'.format(self.server, name))
        return r.text

    def add_note(self, catname, text):
        r = requests.post('{}/categories/{}?text={}'.format(self.server,
                                                            catname, text))
        return r.text

    def delete_category(self, name):
        r = requests.delete('{}/categories/{}'.format(self.server, name))
        return r.text

    def delete_note(self, catname, noteid):
        r = requests.delete('{}/categories/{}/{}'.format(self.server,
                                                         catname, noteid))
        return r.text

    def change_category(self, name, newname):
        r = requests.put('{}/categories/{}?name={}'.format(self.server,
                                                           name, newname))
        return r.text

    def change_note(self, catname, noteid, text):
        r = requests.put('{}/categories/{}/{}?text={}'.format(self.server,
                                                              catname, noteid,
                                                              text))
        return r.text


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


def work_parse(argv):
    parser = createparser()
    namespace = parser.parse_args(argv)

    if namespace.server:
        nsc = NoteServerClient(namespace.server)

        if namespace.command == 'view':
            if namespace.categories and namespace.category is None:
                print(nsc.view_categories())
                return True

            elif namespace.category and namespace.categories is None:
                if namespace.noteid:
                    print(nsc.view_note(namespace.category, namespace.noteid))
                    return True
                else:
                    print(nsc.view_notes(namespace.category))
                    return True

            elif namespace.categories is not None and namespace.category is not None:
                print('Error: use only one of this arguments.'
                      'Enter view -h to see the arguments')
                return False
            else:
                print('Enter view -h to see the arguments')
                return False

        elif namespace.command == 'addcat':
            if namespace.category:
                print(nsc.add_category(namespace.category))
                return True
            else:
                print('Enter addcat -h to see the arguments')
                return False

        elif namespace.command == 'addnote':
            if namespace.note and namespace.catname:
                print(nsc.add_note(namespace.catname, namespace.note))
                return True
            elif namespace.note or namespace.catname:
                print('Error: arguments --note and --category required to delete the note.'
                      'Enter addnote -h to see the arguments')
                return False
            else:
                print('Enter addnote -h to see the arguments')
                return False

        elif namespace.command == 'delcat':
            if namespace.name:
                print(nsc.delete_category(namespace.name))
                return True
            else:
                print('Enter delcat -h to see the arguments')
                return False

        elif namespace.command == 'delnote':
            if namespace.noteid and namespace.catname:
                print(nsc.delete_note(namespace.catname, namespace.noteid))
                return True
            elif namespace.noteid or namespace.catname:
                print('Error: arguments --noteid and --catname required to delete the note.'
                      ' Enter delnote -h for help')
                return False
            else:
                print('Enter delnote -h for help')
                return False

        elif namespace.command == 'changecat':
            if namespace.name and namespace.newname:
                print(nsc.change_category(namespace.name, namespace.newname))
                return True
            elif namespace.name or namespace.newname:
                print('Error: arguments --name and --newname required to change the name of category.'
                      ' Enter changecat -h for help')
                return False
            else:
                print('Enter changecat -h for help')
                return False

        elif namespace.command == 'changenote':
            if namespace.catname and namespace.noteid and namespace.text:
                nsc.change_note(namespace.catname, namespace.noteid, namespace.text)
                return True
            elif namespace.catname or namespace.noteid or namespace.text:
                print('Error: arguments --catname, --noteid and --text'
                      ' required to change the text of note.'
                      'Enter changenote -h to see the arguments')
                return False
            else:
                print('Enter changenote -h to see the arguments')
                return False

        else:
            parser.print_help()
            return False

    else:
        parser.print_help()
        return False


if __name__ == '__main__':
    t = work_parse(sys.argv[1:])
    print(t)
