import random
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

banco_dados = {}
casos_arquivados = {}
tentativas_restantes = 3

def limpar_janela():
    for widget in janela.winfo_children():
        widget.destroy()

def criar_cabecalho(titulo):
    header = ctk.CTkFrame(janela, fg_color="#1e293b", height=50, corner_radius=0)
    header.pack(fill="x", side="top")
    
    lbl_logo = ctk.CTkLabel(header, text="RCS", font=("Arial", 14, "bold"), text_color="#38bdf8", fg_color="#1e293b")
    lbl_logo.pack(side="left", padx=15, pady=10)
    
    lbl_titulo = ctk.CTkLabel(header, text=titulo, font=("Arial", 12, "bold"), text_color="white", fg_color="#1e293b")
    lbl_titulo.pack(side="left", padx=10)


def tela_login():
    limpar_janela()
    criar_cabecalho("Acesso ao Sistema")

    lbl_sub = ctk.CTkLabel(janela, text="Digite suas credenciais", font=("Arial", 12))
    lbl_sub.pack(pady=(30, 15))

    entry_usuario = ctk.CTkEntry(janela, placeholder_text="Usuário", width=220, height=35)
    entry_usuario.pack(pady=8)

    entry_senha = ctk.CTkEntry(janela, placeholder_text="Senha", show="*", width=220, height=35)
    entry_senha.pack(pady=8)

    def autenticar():
        global tentativas_restantes
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if usuario == "admin" and senha == "1234":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            tela_menu()
        else:
            tentativas_restantes -= 1
            if tentativas_restantes > 0:
                messagebox.showwarning("Acesso Negado", f"Usuário ou senha incorretos!\nTentativas restantes: {tentativas_restantes}")
                entry_senha.delete(0, ctk.END)
            else:
                messagebox.showerror("Bloqueio", "Número máximo de tentativas atingido.")
                janela.destroy()

    btn_entrar = ctk.CTkButton(janela, text="Entrar", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", font=("Arial", 11, "bold"), width=220, height=35, command=autenticar)
    btn_entrar.pack(pady=20)


def tela_menu():
    limpar_janela()
    criar_cabecalho("Menu Principal")

    lbl_instrucao = ctk.CTkLabel(janela, text="Selecione uma opção:", font=("Arial", 12))
    lbl_instrucao.pack(pady=20)

    btn1 = ctk.CTkButton(janela, text="1. Registrar Novo Processo", fg_color="#10b981", hover_color="#059669", text_color="white", font=("Arial", 11, "bold"), width=200, height=35, command=tela_registrar)
    btn1.pack(pady=10)

    btn2 = ctk.CTkButton(janela, text="2. Atualizar / Excluir Processo", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", font=("Arial", 11, "bold"), width=200, height=35, command=tela_atualizar)
    btn2.pack(pady=10)

    btn3 = ctk.CTkButton(janela, text="3. Consultar Arquivados", fg_color="#64748b", hover_color="#475569", text_color="white", font=("Arial", 11, "bold"), width=200, height=35, command=tela_arquivados)
    btn3.pack(pady=10)

    btn_logout = ctk.CTkButton(janela, text="Sair da Conta", fg_color="#ef4444", hover_color="#dc2626", text_color="white", font=("Arial", 10, "bold"), width=120, height=30, command=tela_login)
    btn_logout.pack(pady=20)


def tela_registrar():
    limpar_janela()
    criar_cabecalho("Registrar Processo")

    lbl_nome = ctk.CTkLabel(janela, text="Nome do Envolvido: *")
    lbl_nome.pack(pady=(15, 2))
    entry_nome = ctk.CTkEntry(janela, width=300)
    entry_nome.pack(pady=2)

    lbl_crime = ctk.CTkLabel(janela, text="Capitulação do Crime: *")
    lbl_crime.pack(pady=(10, 2))
    entry_crime = ctk.CTkEntry(janela, width=300)
    entry_crime.pack(pady=2)

    lbl_data = ctk.CTkLabel(janela, text="Data do Fato (DD/MM/AAAA): *")
    lbl_data.pack(pady=(10, 2))
    entry_data = ctk.CTkEntry(janela, width=160)
    entry_data.pack(pady=2)

    lbl_perfil = ctk.CTkLabel(janela, text="Qualificação: *")
    lbl_perfil.pack(pady=(10, 2))
    perfil_var = ctk.StringVar(value="Réu")
    menu_perfil = ctk.CTkOptionMenu(janela, variable=perfil_var, values=["Réu", "Vítima", "Testemunha"])
    menu_perfil.pack(pady=2)

    def salvar():
        nome = entry_nome.get()
        crime = entry_crime.get()
        data = entry_data.get()
        perfil = perfil_var.get()

        if nome == "" or crime == "" or data == "":
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        protocolo = str(random.randint(100000, 999999))
        banco_dados[protocolo] = {"nome": nome, "crime": crime, "data": data, "perfil": perfil}
        
        messagebox.showinfo("Sucesso", f"Processo cadastrado!\nProtocolo: {protocolo}")
        tela_menu()

    btn_salvar = ctk.CTkButton(janela, text="Salvar Cadastro", fg_color="#10b981", hover_color="#059669", text_color="white", font=("Arial", 10, "bold"), command=salvar)
    btn_salvar.pack(pady=15)

    btn_voltar = ctk.CTkButton(janela, text="Voltar ao Menu", fg_color="#ef4444", hover_color="#dc2626", text_color="white", command=tela_menu)
    btn_voltar.pack()

def tela_atualizar():
    limpar_janela()
    criar_cabecalho("Atualizar ou Excluir Processo")

    lbl_busca = ctk.CTkLabel(janela, text="Digite o Protocolo:")
    lbl_busca.pack(pady=(15, 2))

    entry_busca = ctk.CTkEntry(janela, width=160)
    entry_busca.pack(pady=2)

    frame_edicao = ctk.CTkFrame(janela)

    lbl_info = ctk.CTkLabel(frame_edicao, text="", font=("Arial", 10, "bold"))
    lbl_info.pack(pady=5)

    lbl_crime_edit = ctk.CTkLabel(frame_edicao, text="Novo Crime:")
    lbl_crime_edit.pack()
    entry_crime_edit = ctk.CTkEntry(frame_edicao, width=280)
    entry_crime_edit.pack(pady=2)

    lbl_perfil_edit = ctk.CTkLabel(frame_edicao, text="Nova Qualificação:")
    lbl_perfil_edit.pack()
    perfil_edit_var = ctk.StringVar(value="Réu")
    menu_perfil_edit = ctk.CTkOptionMenu(frame_edicao, variable=perfil_edit_var, values=["Réu", "Vítima", "Testemunha"])
    menu_perfil_edit.pack(pady=2)

    def buscar():
        prot = entry_busca.get()
        if prot in banco_dados:
            frame_edicao.pack(pady=10, padx=10, fill="x")
            processo = banco_dados[prot]
            
            lbl_info.configure(text=f"Pessoa: {processo['nome']} ({processo['perfil']})")
            entry_crime_edit.delete(0, ctk.END)
            entry_crime_edit.insert(0, processo["crime"])
            perfil_edit_var.set(processo["perfil"])
            
            btn_salvar.configure(command=lambda: salvar_alteracao(prot))
            btn_arquivar.configure(command=lambda: arquivar(prot))
            btn_excluir.configure(command=lambda: excluir(prot))
        else:
            frame_edicao.pack_forget()
            messagebox.showerror("Erro", "Protocolo não encontrado!")

    btn_buscar = ctk.CTkButton(janela, text="Buscar", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", command=buscar)
    btn_buscar.pack(pady=5)

    def salvar_alteracao(prot):
        banco_dados[prot]["crime"] = entry_crime_edit.get()
        banco_dados[prot]["perfil"] = perfil_edit_var.get()
        messagebox.showinfo("Sucesso", "Processo atualizado com sucesso!")
        tela_menu()

    def arquivar(prot):
        processo = banco_dados.pop(prot)
        casos_arquivados[prot] = processo
        messagebox.showinfo("Arquivado", "Processo movido para Arquivados.")
        tela_menu()

    def excluir(prot):
        if messagebox.askyesno("Confirmar", "Deseja apagar este processo?"):
            del banco_dados[prot]
            messagebox.showwarning("Excluído", "Processo apagado.")
            tela_menu()

    btn_salvar = ctk.CTkButton(frame_edicao, text="Salvar", fg_color="#10b981", hover_color="#059669", text_color="white", width=80)
    btn_salvar.pack(side="left", padx=5, pady=10)

    btn_arquivar = ctk.CTkButton(frame_edicao, text="Arquivar", fg_color="#64748b", hover_color="#475569", text_color="white", width=80)
    btn_arquivar.pack(side="left", padx=5, pady=10)

    btn_excluir = ctk.CTkButton(frame_edicao, text="Excluir", fg_color="#ef4444", hover_color="#dc2626", text_color="white", width=80)
    btn_excluir.pack(side="left", padx=5, pady=10)

    btn_voltar = ctk.CTkButton(janela, text="Voltar ao Menu", fg_color="#94a3b8", hover_color="#64748b", text_color="white", command=tela_menu)
    btn_voltar.pack(side="bottom", pady=15)

#Tela de processos arquivados
def tela_arquivados():
    limpar_janela()
    criar_cabecalho("Processos Arquivados")

    texto_area = ctk.CTkTextbox(janela, width=450, height=300)
    texto_area.pack(pady=15)

    if len(casos_arquivados) == 0:
        texto_area.insert(ctk.END, "Nenhum processo arquivado registrado.\n")
    else:
        for prot, dados in casos_arquivados.items():
            linha = f"Protocolo: {prot} | Nome: {dados['nome']} | Crime: {dados['crime']} | Perfil: {dados['perfil']} | Data: {dados['data']}\n"
            texto_area.insert(ctk.END, linha)

    texto_area.configure(state="disabled")

    btn_voltar = ctk.CTkButton(janela, text="Voltar ao Menu", fg_color="#94a3b8", hover_color="#64748b", text_color="white", command=tela_menu)
    btn_voltar.pack(pady=10)


janela = ctk.CTk()
janela.title("Sistema RCS")
janela.geometry("500x550")

tela_login()

janela.mainloop()