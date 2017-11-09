from flask import Flask, request, render_template
from flask_restful import reqparse, abort, Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import routes

db = create_engine('sqlite:///kantin.db')
app = Flask(__name__)
api = Api(app)

class Warung(Resource):
    def get(self):
        conn = db.connect() # connect to database
        query = conn.execute("select * from warung") # This line performs query and returns json result
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} # Fetches first column that is Employee ID

class WarungDetails(Resource):
    def get(self, id):
        conn = db.connect()
        warung = conn.execute("select * from warung where id=%d" %int(id)).fetchone()
        pedagang=conn.execute("select * from pedagang where warung_id=%d" %int(id))
        menu=conn.execute("select makanan.nama,menu.harga,makanan.tipe from menu join warung on menu.warung_id=warung.id join makanan on menu.makanan_id=makanan.id where warung.id=%d" %int(id))
        results = {
            'data':{
                'warung': {
                    'id':warung['id'],
                    'nama':warung['nama'],
                    'rating':warung['rating']
                },
                'pedagang':[dict(zip(tuple (pedagang.keys()) ,i)) for i in pedagang.cursor],
                'menu':[dict(zip(tuple (menu.keys()) ,i)) for i in menu.cursor],
            }
        }
        return jsonify(results);

class Pedagang(Resource):
    def get(self):
        conn = db.connect()
        query = conn.execute("select * from pedagang")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def post(self):
        json=request.get_json(force=True)
        conn=db.connect()
        data=json['pedagangs']
        for pedagang in data:
            query = conn.execute("insert into pedagang(nama,jenis_kelamin,tanggal_lahir,warung_id) values('%s','%s','%s','%s')" % (pedagang['nama'],pedagang['jenis_kelamin'],pedagang['tanggal_lahir'],pedagang['warung_id']))

        return data;

class PedagangDetails(Resource):
    def get(self, id):
        conn=db.connect()
        query=conn.execute("select * from pedagang where id=%d" %int(id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

if __name__ == '__main__':
     app.run(port='5000')
