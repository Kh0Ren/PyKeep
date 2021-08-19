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
class Keeps(db.Entity):
    # Первичный ключ
    id = orm.PrimaryKey(int, auto=True)
    # Заметка пользователя
    keep = orm.Required(str)


# Привязываю объявленную сущность к БД
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
# создаю таблицу БД, где будут храниться атрибуты сущности Keeps
db.generate_mapping(create_tables=True)


# Создаю функцию, которая будет работать со списком заметок
# И привязываю ее к URL-адресу
# Объявляю HTTP-методы,
@app.route('/keeps', methods=['GET', 'POST'])
def request_keeps():
    if request.method == 'GET':
        try:
            keeps_list = orm.select(k for k in Keeps)
            keeps = {
                "data": []
            }
            for i in keeps_list:
                keeps["data"].append({"id": i.id, "keep": i.keep})
            return keeps, 200
        except Exception as error:
            return {
                "status": "error",
                "message": str(error)
            }, 500

    if request.method == 'POST':
        try:
            k = Keeps(keep=request.args['keep'])
            return {"id": k.id, "keep": k.keep}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500


@app.route('/keeps/<int:keep_id>', methods=['GET', 'PUT', 'DELETE'])
def request_keep(keep_id):
    if request.method == 'GET':
        try:
            k = Keeps[keep_id]
            return {k.id: k.keep}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500
    if request.method == 'PUT':
        try:
            k = Keeps.get(id=id)
            k.keep = request.args['keep']
            return {"status": "OK", "message": "updated"}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500
    if request.method == 'DELETE':
        try:
            Keeps[id].delete()
            return {"status": "OK", "message": "deleted"}, 200
        except Exception as error:
            return {
                       "status": "error",
                       "message": str(error)
                   }, 500


app.run()
