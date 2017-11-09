from flask import request
from flask_restful import reqparse, abort, Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from app import app

db = create_engine('sqlite:///kantin.db')
api = Api(app)

class Warung(Resource):
    def get(self):
        conn = db.connect()
        query = conn.execute("select * from warung")
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

    def post(self):
        json=request.get_json(force=True)
        conn=db.connect()
        data=json['warung']
        for warung in data:
            query = conn.execute("insert into warung(nama,rating) values('%s','%s')" % (warung['nama'],warung['rating']))

        return data;


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

    def put(self, id):
        json=request.get_json(force=True)
        conn=db.connect()
        nama=json['nama'] if ('nama' in json) else ''
        rating=json['rating'] if ('rating' in json) else ''
        if nama!="":
            query = conn.execute("update warung set nama='%s' where id='%s'" %(nama,id))
        if rating!="":
            query = conn.execute("update warung set rating='%s' where id='%s'" %(rating,id))

        return json
    def delete(self,id):
        conn=db.connect()
        query=conn.execute("delete from warung where id=%d" %int(id))
        if query:
            return jsonify({"message":"warung id %d deleted" %int(id)})

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

    def put(self, id):
        json=request.get_json(force=True)
        conn=db.connect()

        if 'nama' in json:
            data=json['nama']
            query = conn.execute("update pedagang set nama='%s' where id='%s'" %(data,id))
        if 'jenis_kelamin' in json:
            data=json['jenis_kelamin']
            query = conn.execute("update pedagang set jenis_kelamin='%s' where id='%s'" %(data,id))
        if 'tanggal_lahir' in json:
            data=json['tanggal_lahir']
            query = conn.execute("update pedagang set jenis_kelamin='%s' where id='%s'" %(data,id))
        if 'warung_id' in json:
            data=json['warung_id']
            query = conn.execute("update pedagang set warung_id='%s' where id='%s'" %(data,id))

        return json

    def delete(self,id):
        conn=db.connect()
        query=conn.execute("delete from pedagang where id=%d" %int(id))
        if query:
            return jsonify({"message":"pedagang id %d deleted" %int(id)})

api.add_resource(Warung, '/api/warung')
api.add_resource(Pedagang, '/api/pedagang')
api.add_resource(WarungDetails,'/api/warung/<id>')
api.add_resource(PedagangDetails, '/api/pedagang/<id>')

# if __name__ == '__main__':
#      app.run(port='5000')
