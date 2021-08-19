from flask import Flask, request
from pony.flask import Pony
from pony import orm

app = Flask(__name__)
Pony(app)
db = orm.Database()


class Keeps(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    keep = orm.Required(str)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

with orm.db_session:
    Keeps.select().show()


@app.route('/keeps', methods=['GET', 'POST'])
def request_keeps():
    if request.method == 'GET':
        try:
            keeps_list = orm.select(k for k in Keeps)
            dict = {}
            for i in keeps_list:
                dict[i.id] = i.keep
            return dict, 200
        except Exception:
            return 'Error'

    if request.method == 'POST':
        try:
            print(request.args['keep'])
            Keeps(keep=request.args['keep'])
            return 'Ok'
        except Exception:
            return 'Error'


@app.route('/keeps/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def request_keep(id):
    if request.method == 'GET':
        try:
            k = Keeps.get(id=id)
            return k.keep
        except Exception:
            return 'Error 404'
    if request.method == 'PUT':
        try:
            k = Keeps.get(id=id)
            k.keep = request.args['keep']
            return 'Ok'
        except Exception:
            return 'Error 404'
    if request.method == 'DELETE':
        try:
            Keeps[id].delete()
            return 'Ok'
        except Exception:
            return 'Error 404'


app.run()
