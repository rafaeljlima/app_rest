from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        # Rota para listar todos os hoteis cadastrados
        # Executa a query SELECT * FROM Hoteis
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank!")
    atributos.add_argument('estrelas', type = float, required=True, help="The field 'estrelas' cannot be left blank!")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        # Rota para buscar um hotel pelo ID
        # Executa a query SELECT * FROM Hoteis WHERE hotel_id = hotel_id
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404
    
    @jwt_required()
    def post(self, hotel_id):
        # Rota para criar um novo hotel
        # Executa a query INSERT INTO Hoteis (hotel_id, nome, estrelas, diaria, cidade) VALUES (hotel_id, nome, estrelas, diaria, cidade)
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)},400
        
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error occurred while inserting the hotel."}, 500
        hotel.save_hotel()
        return hotel.json()
    
    @jwt_required()
    def put(self, hotel_id):
        # Rota para atualizar um hotel pelo ID
        # Executa a query UPDATE Hoteis SET nome = nome, estrelas = estrelas, diaria = diaria, cidade = cidade WHERE hotel_id = hotel_id
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error occurred while inserting the hotel."}, 500
        hotel.save_hotel()
        return hotel.json(), 201
    
    @jwt_required()
    def delete(self, hotel_id):
        # Rota para deletar um hotel pelo ID
        # Executa a query DELETE FROM Hoteis WHERE hotel_id = hotel_id
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An internal error occurred while deleting the hotel."}, 500
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found'}, 404
