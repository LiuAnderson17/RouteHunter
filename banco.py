import sqlite3

class BancoDeDados:
    def __init__(self, nome_banco="clientes.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()

        # Cria as tabelas se não existirem
        self.cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, endereco TEXT)")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chave_api (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 chave TEXT NOT NULL)''')
        self.conexao.commit()

    def adicionar_cliente(self, nome, endereco):
        self.cursor.execute("INSERT INTO clientes (nome, endereco) VALUES (?, ?)", (nome, endereco))
        self.conexao.commit()

    def obter_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def atualizar_cliente(self, id, nome, endereco):
        self.cursor.execute("UPDATE clientes SET nome = ?, endereco = ? WHERE id = ?", (nome, endereco, id))
        self.conexao.commit()

    def excluir_cliente(self, id):
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        self.conexao.commit()

    def obter_cliente_por_nome(self, nome):
        self.cursor.execute("SELECT * FROM clientes WHERE nome = ?", (nome,))
        return self.cursor.fetchone()

    def adicionar_chave_api(self, chave):
        self.cursor.execute('DELETE FROM chave_api')  # Remove qualquer chave existente
        self.cursor.execute('INSERT INTO chave_api (chave) VALUES (?)', (chave,))
        self.conexao.commit()

    def obter_chave_api(self):
        self.cursor.execute('SELECT chave FROM chave_api LIMIT 1')
        chave = self.cursor.fetchone()
        return chave[0] if chave else None

    def deletar_chave_api(self):
        self.cursor.execute('DELETE FROM chave_api')  # Remove a chave cadastrada
        self.conexao.commit()
        #messagebox.showinfo("Informação", "Chave da API deletada com sucesso!")

