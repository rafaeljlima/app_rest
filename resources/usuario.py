from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST
#from werkzeug.security import safe_str_cmp

# Define the parameters for user registration
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

# Define the class for user management
class User(Resource):

    # Method to get user information
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404
   
    # Method to delete user
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": "An internal error occurred while deleting the User."}, 500
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404
    
# Define the class for user registration
class UserRegister(Resource):

    # Method to register a new user
    def post(self):
        
        dados = atributos.parse_args() # Parse the arguments to get the user data

        if UserModel.find_by_login(dados['login']): # Check if the login already exists
            return {"message": "The login '{}' already exists.".format(dados['login'])}, 400

        user = UserModel(**dados) # Create a new user object
        user.save_user() # Save the user to the database
        return {'message': 'User created successfully.'}, 201
    
# Define the class for user login
class UserLogin(Resource):

    # Method to log in the user
    @classmethod
    def post(cls):
        dados = atributos.parse_args() # Parse the arguments to get the user data

        user = UserModel.find_by_login(dados['login']) # Find the user by login

        if user and user.senha == dados['senha']: # Check if the password is correct
            token_de_acesso = create_access_token(identity=user.user_id) # Generate an access token
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401
    
# Define the class for user logout
class UserLogout(Resource):
    # Method to log out the user
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # Get the JWT ID
        BLACKLIST.add(jwt_id) # Add the JWT ID to the blacklist
        return {'message': 'Logged out successfully!'},200
