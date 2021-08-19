from flask import Flask
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
    # Keeps(keep='Buy vodka and cigarettes')
    Keeps.select().show()


@app.route('/keeps')
def return_keeps():
    keeps_list = orm.select(k for k in Keeps)
    for i in keeps_list:
        return i.keep


@app.route('/keeps/<int:id>')
def return_keep(id):
    k = Keeps.get(id=id)
    return k.keep


app.run()
