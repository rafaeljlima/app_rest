from flask import Flask, jsonify
from flask_restful import  Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from sql_alchemy import banco
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
    

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Rafael/Documents/Aulas/Rest API Python Flask/Exercicio/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  Exemplo: expira em 1 hora

api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST 

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401

banco.init_app(app)

    
with app.app_context():
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)