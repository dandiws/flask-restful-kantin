from flask import Flask, render_template
from flask_restful import Api
from app import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Warung, '/warung') # Route_1
api.add_resource(Pedagang, '/pedagang') # Route_2
api.add_resource(WarungDetails,'/warung/<id>')
api.add_resource(PedagangDetails, '/pedagang/<id>') # Route_3

@app.route('/')
def index():
    return render_template("index.html")
