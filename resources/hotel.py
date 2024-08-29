from flask import jsonify, request
from flask_restful import Resource
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset}

class Hoteis(Resource):
    def get(self):
        # Obtendo os parâmetros da URL
        args = request.args
        try:
            # Convertendo parâmetros para float onde aplicável
            dados_validos = {
                'cidade': args.get('cidade'),
                'estrelas_min': float(args.get('estrelas_min', 0)),
                'estrelas_max': float(args.get('estrelas_max', 5)),
                'diaria_min': float(args.get('diaria_min', 0)),
                'diaria_max': float(args.get('diaria_max', 10000)),
                'limit': int(args.get('limit', 50)),
                'offset': int(args.get('offset', 0))
            }
        except ValueError as e:
            return {"message": f"Invalid parameter value: {e}"}, 400
        
        parametros = normalize_path_params(**dados_validos)

        try:
            # Construindo a consulta
            query = HotelModel.query.filter(
                HotelModel.estrelas.between(parametros['estrelas_min'], parametros['estrelas_max']),
                HotelModel.diaria.between(parametros['diaria_min'], parametros['diaria_max'])
            )
            if parametros.get('cidade'):
                query = query.filter(HotelModel.cidade == parametros['cidade'])
            
            query = query.limit(parametros['limit']).offset(parametros['offset'])
            
            hoteis = query.all()

            # Verificando se os dados foram encontrados
            if not hoteis:
                return {'message': 'No hotels found matching the criteria.'}, 404

            # Convertendo os resultados para JSON
            response = {'hoteis': [hotel.json() for hotel in hoteis]}
            return jsonify(response)

        except SQLAlchemyError as e:
            print(f"Erro na consulta: {e}")
            return {"message": "An internal error occurred while querying hotels."}, 500
        
class Hotel(Resource):
    atributos = {
        'nome': {'type': str, 'required': True, 'help': "The field 'nome' cannot be left blank!"},
        'estrelas': {'type': float},
        'diaria': {'type': float},
        'cidade': {'type': str}
    }

    def get(self, hotel_id):
        # Rota para buscar um hotel pelo ID
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404

    @jwt_required()
    def post(self, hotel_id):
        # Rota para criar um novo hotel
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists."}, 400
        
        dados = request.get_json()
        if not all(field in dados for field in ['nome']):
            return {"message": "The field 'nome' cannot be left blank!"}, 400
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except SQLAlchemyError as e:
            print(f"Erro ao salvar o hotel: {e}")
            return {"message": "An internal error occurred while inserting the hotel."}, 500
        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        # Rota para atualizar um hotel pelo ID
        dados = request.get_json()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except SQLAlchemyError as e:
                print(f"Erro ao atualizar o hotel: {e}")
                return {"message": "An internal error occurred while updating the hotel."}, 500
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except SQLAlchemyError as e:
            print(f"Erro ao salvar o hotel: {e}")
            return {"message": "An internal error occurred while inserting the hotel."}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        # Rota para deletar um hotel pelo ID
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except SQLAlchemyError as e:
                print(f"Erro ao deletar o hotel: {e}")
                return {"message": "An internal error occurred while deleting the hotel."}, 500
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found'}, 404