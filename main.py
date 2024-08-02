import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from banco import BancoDeDados


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Hunter")
        self.banco = BancoDeDados()
        self.chave_api = ""  # Chave da API inicialmente vazia
        self.criar_interface()

    def criar_interface(self):
        self.tabs = ttk.Notebook(self.root)

        self.tab_cadastro = ttk.Frame(self.tabs)
        self.tab_visualizacao = ttk.Frame(self.tabs)
        self.tab_rotas = ttk.Frame(self.tabs)
        self.tab_configuracao = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_cadastro, text='Cadastro de Clientes')
        self.tabs.add(self.tab_visualizacao, text='Visualizar Clientes')
        self.tabs.add(self.tab_rotas, text='Pesquisar Rotas')
        self.tabs.add(self.tab_configuracao, text='Configurar API')
        self.tabs.pack(expand=1, fill="both")

        self.criar_tela_cadastro()
        self.criar_tela_visualizacao()
        self.criar_tela_rotas()
        self.criar_tela_configuracao_api()

        # Estilização das abas
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", background="#f0f0f0",
                        foreground="#333333")  # Define a cor de fundo e de texto das abas do Notebook

        # Estilização do botão
        style = ttk.Style()
        style.configure("TButton", background="#00ff00", foreground="#000000", font=("Arial", 10, "bold"))
        style.configure("Excluir.TButton", background="#D2691E", foreground="#000000", font=("Arial", 10, "bold"))


    def criar_tela_cadastro(self):
        frame = ttk.Frame(self.tab_cadastro, padding="10")
        frame.pack(fill="x", expand=True)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = ttk.Entry(frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Endereço:").grid(row=1, column=0, sticky="w")
        self.endereco_entry = ttk.Entry(frame, width=50)
        self.endereco_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Adicionar Cliente", command=self.adicionar_cliente).grid(row=2, columnspan=2, pady=10)

    def criar_tela_visualizacao(self):
        self.clientes_tree = ttk.Treeview(self.tab_visualizacao, columns=("ID", "Nome", "Endereço"), show='headings')
        self.clientes_tree.heading("ID", text="ID")
        self.clientes_tree.heading("Nome", text="Nome")
        self.clientes_tree.heading("Endereço", text="Endereço")
        self.clientes_tree.pack(expand=True, fill="both", pady=10, padx=10)

        self.clientes_tree.bind("<Double-1>", self.editar_cliente)

        ttk.Button(self.tab_visualizacao, text="Excluir Cliente", command=self.excluir_cliente,
                   style="Excluir.TButton").pack(pady=5)
        ttk.Button(self.tab_visualizacao, text="Visualizar Marcadores de Clientes",
                   command=self.visualizar_marcadores_clientes).pack(pady=5)

        self.carregar_clientes()

        # Ajustando as colunas do Treeview
        self.clientes_tree.column("ID", width=70, anchor=tk.CENTER)
        self.clientes_tree.column("Nome", width=100)
        self.clientes_tree.column("Endereço", width=400)

    def criar_tela_rotas(self):
        frame = ttk.Frame(self.tab_rotas, padding="10")
        frame.pack(fill="x", expand=True)

        ttk.Label(frame, text="Origem:").grid(row=0, column=0, sticky="w")
        self.origem_combobox = ttk.Combobox(frame, width=47)
        self.origem_combobox.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Destino:").grid(row=1, column=0, sticky="w")
        self.destino_combobox = ttk.Combobox(frame, width=47)
        self.destino_combobox.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Pesquisar Rota", command=self.pesquisar_rota).grid(row=2, columnspan=2, pady=10)

        self.carregar_clientes_combobox()


    def criar_tela_configuracao_api(self):
        frame = ttk.Frame(self.tab_configuracao, padding="10")
        frame.pack(fill="x", expand=True)

        ttk.Label(frame, text="Chave da API do Google:").grid(row=0, column=0, sticky="w")
        self.chave_api_entry = ttk.Entry(frame, width=50)
        self.chave_api_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Salvar Chave", command=self.salvar_chave_api).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Excluir Chave", command=self.deletar_chave_api,style="Excluir.TButton").grid(row=2, column=0, columnspan=2, pady=10)

        #ttk.Label(frame, text="").grid(row=3, column=0)  # Espaço entre os botões


        chave_salva = self.banco.obter_chave_api()
        if chave_salva:
            self.chave_api_entry.insert(0, chave_salva)



    def salvar_chave_api(self):
        print("Salvando chave...")
        chave = self.chave_api_entry.get()
        if chave:
            self.banco.adicionar_chave_api(chave)
            print("Chave salva:", self.banco.obter_chave_api())  # Verifica se a chave foi salva corretamente
            messagebox.showinfo("Informação", "Chave da API salva com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma chave válida")

    def deletar_chave_api(self):
        confirmar = messagebox.askokcancel("Confirmar Deleção", "Tem certeza que deseja deletar a chave da API?")
        if confirmar:
            self.banco.deletar_chave_api()
            self.chave_api = None
            self.chave_api_entry.delete(0, tk.END)
            messagebox.showinfo("Informação", "Chave da API deletada com sucesso!")



    def visualizar_todos_no_mapa(self):
        for cliente in self.banco.obter_clientes():
            endereco = cliente[2]
            url = f"https://www.google.com/maps/search/?api=1&query={endereco}"
            webbrowser.open_new_tab(url)

    def adicionar_cliente(self):
        nome = self.nome_entry.get()
        endereco = self.endereco_entry.get()

        if nome and endereco:
            self.banco.adicionar_cliente(nome, endereco)
            self.nome_entry.delete(0, tk.END)
            self.endereco_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso")
            self.carregar_clientes()
            self.carregar_clientes_combobox()
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos")

    def carregar_clientes(self):
        for i in self.clientes_tree.get_children():
            self.clientes_tree.delete(i)

        for cliente in self.banco.obter_clientes():
            self.clientes_tree.insert("", "end", values=cliente)

    def carregar_clientes_combobox(self):
        clientes = self.banco.obter_clientes()
        nomes = [cliente[1] for cliente in clientes]
        self.origem_combobox['values'] = nomes
        self.destino_combobox['values'] = nomes

    def editar_cliente(self, event):
        item = self.clientes_tree.selection()[0]
        cliente = self.clientes_tree.item(item, "values")

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Editar Cliente")

        ttk.Label(self.edit_window, text="Nome:").grid(row=0, column=0, sticky="w")
        self.edit_nome_entry = ttk.Entry(self.edit_window, width=50)
        self.edit_nome_entry.grid(row=0, column=1, padx=10, pady=5)
        self.edit_nome_entry.insert(0, cliente[1])

        ttk.Label(self.edit_window, text="Endereço:").grid(row=1, column=0, sticky="w")
        self.edit_endereco_entry = ttk.Entry(self.edit_window, width=50)
        self.edit_endereco_entry.grid(row=1, column=1, padx=10, pady=5)
        self.edit_endereco_entry.insert(0, cliente[2])

        ttk.Button(self.edit_window, text="Salvar", command=lambda: self.atualizar_cliente(cliente[0])).grid(row=2,
                                                                                                             columnspan=2,
                                                                                                             pady=10)

    def atualizar_cliente(self, id):
        nome = self.edit_nome_entry.get()
        endereco = self.edit_endereco_entry.get()

        if nome and endereco:
            self.banco.atualizar_cliente(id, nome, endereco)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso")
            self.edit_window.destroy()
            self.carregar_clientes()
            self.carregar_clientes_combobox()
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos")

    def excluir_cliente(self):
        item = self.clientes_tree.selection()
        if item:
            cliente = self.clientes_tree.item(item, "values")
            confirmar = messagebox.askokcancel("Confirmar Exclusão",
                                               f"Tem certeza que deseja excluir o cliente {cliente[1]}?")
            if confirmar:
                self.banco.excluir_cliente(cliente[0])
                self.carregar_clientes()

    def pesquisar_rota(self):
        origem_nome = self.origem_combobox.get()
        destino_nome = self.destino_combobox.get()

        if origem_nome and destino_nome:
            origem = self.banco.obter_cliente_por_nome(origem_nome)
            destino = self.banco.obter_cliente_por_nome(destino_nome)

            if origem and destino:
                origem_endereco = origem[2]
                destino_endereco = destino[2]

                if self.chave_api:
                    url = f"https://www.google.com/maps/dir/?api=1&key={self.chave_api}&origin={origem_endereco}&destination={destino_endereco}"
                else:
                    url = f"https://www.google.com/maps/dir/{origem_endereco}/{destino_endereco}"

                webbrowser.open_new_tab(url)
            else:
                messagebox.showwarning("Aviso", "Cliente de origem ou destino não encontrado")
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione a origem e o destino")

    def visualizar_marcadores_clientes(self):
        chave_api = self.banco.obter_chave_api()
        print("Chave obtida:", chave_api)  # Verifica se a chave foi obtida corretamente

        if chave_api:
            url = f"https://www.google.com/maps/search/?api=1&key={chave_api}&query="
            for cliente in self.banco.obter_clientes():
                endereco = cliente[2]
                url += endereco + "|"
            webbrowser.open_new_tab(url)
        else:
            messagebox.showerror("Erro","Chave da API não cadastrada. Por favor, configure a chave da API na aba de Configuração.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
