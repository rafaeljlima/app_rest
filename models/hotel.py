from sql_alchemy import banco

class HotelModel(banco.Model): #Classe que representa a tabela 'hoteis' no banco de dados.
    
    __tablename__ = 'hoteis'

    # Atributos da classe
    hotel_id = banco.Column(banco.String, primary_key=True)  # Chave primária do hotel
    nome = banco.Column(banco.String(80))  # Nome do hotel
    estrelas = banco.Column(banco.Float(precision=1))  # Número de estrelas do hotel
    diaria = banco.Column(banco.Float(precision=2))  # Valor da diária do hotel
    cidade = banco.Column(banco.String(40))  # Cidade onde o hotel está localizado

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        #Construtor da classe HotelModel.
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }
    
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # SELECT * FROM hoteis WHERE hotel_id = hotel_id
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        """
        Salva o objeto da classe HotelModel no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        """
        Atualiza os atributos do objeto da classe HotelModel.

        Args:
            nome (str): Novo nome do hotel.
            estrelas (float): Novo número de estrelas do hotel.
            diaria (float): Nova diária do hotel.
            cidade (str): Nova cidade onde o hotel está localizado.
        """
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        """
        Exclui o objeto da classe HotelModel do banco de dados.
        """
        banco.session.delete(self)
        banco.session.commit()
