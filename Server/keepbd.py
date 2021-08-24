# Импорт нужных библиотек для создания сервера и БД
from flask import Flask, request
from pony.flask import Pony
from pony import orm

# Создаю сервер
app = Flask(__name__)
# Интегрирую сервер с будущей БД
Pony(app)
# Создаю БД
db = orm.Database()


# Определяю сущность БД и ее атрибуты
class Note(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    text = orm.Optional(str)
    category = orm.Required('Category')


class Category(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Optional(str, unique=True)
    notes = orm.Set(Note)


# Привязываю объявленную сущность к БД
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
# создаю таблицу БД, где будут храниться атрибуты сущности Notes
db.generate_mapping(create_tables=True)


@app.route('/categories', methods=['GET', 'POST'])
def request_category():
    if request.method == 'GET':
        try:
            cat_list = orm.select(c for c in Category)
            categories = {
                "data": []
                }
            for i in cat_list:
                categories["data"].append({"id": i.id, "name": i.name})
            return categories, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500

    if request.method == 'POST':
        try:
            c = Category(name=request.args['name'])
            db.commit()
            return {"id": c.id, "name": c.name}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500


# Создаю функцию, которая будет работать со списком заметок
# И привязываю ее к URL-адресу
# Объявляю HTTP-методы,
@app.route('/categories/<category>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_notes(category):
    if request.method == 'GET':
        try:
            notes_list = orm.select(n for n in Note if n.category.name == category)
            notes = {
                "data": []
            }
            for i in notes_list:
                notes["data"].append({"id": i.id, "text": i.text})
            return notes, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500

    if request.method == 'POST':
        try:
            c = Category.get(name=category)
            n = Note(text=request.args['text'], category=c.id)

            db.commit()

            return {"id": n.id, "text": n.text}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500

    if request.method == 'PUT':
        try:
            c = Category.get(name=category)
            c.name = request.args['name']
            return {"status": "OK", "message": "updated"}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500

    if request.method == 'DELETE':
        try:
            c = Category.get(name=category)
            c.delete()
            return {"status": "OK", "message": "deleted"}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500


@app.route('/categories/<category>/<int:note_id>', methods=['GET', 'PUT', 'DELETE'])
def request_note(category, note_id):
    if request.method == 'GET':
        try:
            c = Category.get(name=category)
            n = Note.get(id=note_id, category=c.id)
            return {"id": n.id, "text": n.text}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500
    if request.method == 'PUT':
        try:
            c = Category.get(name=category)
            n = Note.get(id=note_id, category=c.id)
            n.text = request.args['text']
            return {"status": "OK", "message": "updated"}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500
    if request.method == 'DELETE':
        try:
            c = Category.get(name=category)
            n = Note.get(id=note_id, category=c.id)
            n.delete()
            return {"status": "OK", "message": "deleted"}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500


app.run()
