from sql_alchemy import banco

class UserModel(banco.Model):
    # Define o nome da tabela no banco de dados
    __tablename__ = 'usuarios'

    # Define as colunas da tabela
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    # Construtor da classe
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    # Define um método que retorna os dados da instância da classe em formato JSON
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }
    
    # Define um método de classe que retorna um objeto da classe com base no ID fornecido
    @classmethod
    def find_user(cls, user_id):
        # Consulta de banco de dados para buscar um objeto com base no ID fornecido
        user = cls.query.filter_by(user_id=user_id).first() # SELECT * FROM Usuarios WHERE user_id = user_id
        if user:
            return user
        return None
    
    # Define um método de classe que retorna um objeto da classe com base no login fornecido
    @classmethod
    def find_by_login(cls, login):
        # Consulta de banco de dados para buscar um objeto com base no login fornecido
        user = cls.query.filter_by(login=login).first() # SELECT * FROM Usuarios WHERE login = login
        if user:
            return user
        return None

    # Define um método para salvar a instância da classe no banco de dados
    def save_user(self):
        # Adiciona a instância da classe à sessão do banco de dados
        banco.session.add(self)
        # Faz o commit das alterações no banco de dados
        banco.session.commit()

    # Define um método para excluir a instância da classe do banco de dados
    def delete_user(self):
        # Exclui a instância da classe da sessão do banco de dados
        banco.session.delete(self)
        # Faz o commit das alterações no banco de dados
        banco.session.commit()
