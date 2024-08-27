from flask import Flask
from flask_restful import  Api
from resources.hotel import Hoteis, Hotel
from sql_alchemy import banco
    

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Rafael/Documents/Aulas/Rest API Python Flask/Exercicio/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

banco.init_app(app)

    
with app.app_context():
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__':
    app.run(debug=True)