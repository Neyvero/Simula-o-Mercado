# ---------------------------------------------------Importações----------------------------------------------------------------
import customtkinter as ctk
import json
import os
from tkinter import messagebox, Listbox, END
# ---------------------------------------------Configurações do Tkinter---------------------------------------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
# ----------------------------------------------------Dicionário----------------------------------------------------------------
sessao = {
    "Hortifruti": sorted([("Banana", 3.50), ("Maçã", 4.00), ("Tomate", 5.00), ("Uva", 7.90)]),
    "Bebidas": sorted([("Água", 2.00), ("Cerveja", 5.50), ("Suco", 4.80)]),
    "Limpeza": sorted([("Detergente", 2.30), ("Sabão em pó", 8.00), ("Vassoura", 9.50)]),
    "Padaria": sorted([("Pão francês", 0.80), ("Bolo", 12.00), ("Rosquinha", 3.50)]),
    "Açougue": sorted([("Alcatra", 39.90), ("Frango", 12.50)]),
    "Mercearia": sorted([("Arroz", 25.90), ("Feijão", 8.50), ("Café", 12.00)]),
    "Laticínios": sorted([("Leite", 5.40), ("Queijo", 14.50)]),
    "Higiene Pessoal": sorted([("Sabonete", 2.00), ("Shampoo", 10.00)]),
    "Congelados": sorted([("Pizza congelada", 19.90), ("Sorvete", 21.00)])
}
# -------------------------------------------------Lista do Carrinho------------------------------------------------------------
carrinho = []
historico = []
# ----------------------------------------------Função de Busca Binária---------------------------------------------------------


def busca_produto(sessao, produto):
    esquerda, direita = 0, len(sessao) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        nome = sessao[meio][0].lower()
        if nome == produto.lower():
            return sessao[meio]
        elif nome < produto.lower():
            esquerda = meio + 1
        else:
            direita = meio - 1
    return None
# ----------------------------------------------Função de atualizar sessoes---------------------------------------------------------


def att_produto(sessao_nome):
    text_result.delete("1.0", "end")
    lista_produto.delete(0, ctk.END)
    for nome, preco in sessao[sessao_nome]:
        texto = f"{nome} - R$ {preco:.2f}"
        lista_produto.insert(ctk.END, texto)
# ----------------------------------------------Função de adicionar ao carrinho-------------------------------------------------------


def add_carrinho():
    selecao = lista_produto.curselection()
    if selecao:
        item = lista_produto.get(selecao[0])
        carrinho.append(item)
        lista_carrinho.insert(ctk.END, item)
        att_total()
        salvar_carrinho()

# -------------------------------------------Função de remover item do carrinho---------------------------------------------------------


def remover_item():
    selecao = lista_carrinho.curselection()
    if selecao:
        item = lista_carrinho.get(selecao[0])
        if item in carrinho:
            carrinho.remove(item)
            lista_carrinho.delete(selecao[0])
        att_total()
        salvar_carrinho()

# ------------------------------------------------Função de remover tudo do carrinho------------------------------------------------------------------


def limpar_carrinho():
    carrinho.clear()
    lista_carrinho.delete(0, ctk.END)
    att_total()
    salvar_carrinho()

# ------------------------------------------------Função de somar preços------------------------------------------------------------------


def att_total():
    total = 0
    for item in carrinho:
        try:
            preco = float(item.split("R$")[1].strip())
            total += preco
        except:
            continue
    label_total.configure(text=f"Total: R$ {total:.2f}")
# --------------------------------------------Função de finalizar compras-----------------------------------------------------------------


def finalizar_compra():
    if not carrinho:
        messagebox.showwarning("Tem certeza?", "O carrinho esta vazio.")
        return
    total = sum(float(item.split("R$")[1]) for item in carrinho)

    salvar_historico(carrinho.copy(), total)

    messagebox.showinfo(
        "Compra finalizada.", f"Obrigado por comprar no Olimpo! Compra de R$: {total:.2f}")
    carrinho.clear()
    lista_carrinho.delete(0, ctk.END)
    att_total()
    salvar_carrinho()


# ----------------------------------Salvar Carrinho---------------------------------------------
ARQUIVO_CARRINHO = "carrinho.json"


def salvar_carrinho():
    try:
        with open(ARQUIVO_CARRINHO, "w", encoding="utf-8") as f:
            json.dump(carrinho, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar o carrinho: {e}")


def carregar_carrinho():
    if not os.path.exists(ARQUIVO_CARRINHO):
        return
    try:
        with open(ARQUIVO_CARRINHO, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                # Arquivo vazio, não faz nada
                return
            dados = json.loads(conteudo)
            carrinho.clear()
            carrinho.extend(dados)

            lista_carrinho.delete(0, ctk.END)
            for item in carrinho:
                lista_carrinho.insert(ctk.END, item)

            att_total()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o carrinho: {e}")


# -----------------------------Historico Carrinho------------------------------------


ARQUIVO_HISTORICO = "historico.json"


def salvar_historico(itens, total):
    historico = []
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except:
            historico = []

    historico.append({
        "itens": itens,
        "total": total
    })

    try:
        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar histórico: {e}")


def mostrar_historico():
    if not os.path.exists(ARQUIVO_HISTORICO):
        messagebox.showinfo("Histórico", "Nenhuma compra registrada ainda.")
        return

    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            historico = json.load(f)

        if not historico:
            messagebox.showinfo(
                "Histórico", "Nenhuma compra registrada ainda.")
            return

        texto = ""
        for i, compra in enumerate(historico, 1):
            itens = "\n".join(compra["itens"])
            total = compra["total"]
            texto += f"Compra {i}:\n{itens}\nTotal: R$ {total:.2f}\n\n"

        janela_historico = ctk.CTkToplevel()
        janela_historico.title("Histórico de Compras")
        janela_historico.geometry("400x400")

        caixa_texto = ctk.CTkTextbox(janela_historico, width=380, height=380)
        caixa_texto.pack(padx=10, pady=10)
        caixa_texto.insert("0.0", texto)
        caixa_texto.configure(state="disabled")  # só leitura

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler histórico: {e}")


# -------------------------------------Execução da função da Busca Binária--------------------------------------------------------------------


def buscar():
    try:
        produto = entry_produto.get()
        for nome_sessao, lista_produtos in sessao.items():
            resultado = busca_produto(lista_produtos, produto)
            if resultado:
                texto = f"Produto: {resultado[0]}, Preço: R$ {resultado[1]:.2f}, Sessão: {nome_sessao}"
                text_result.insert("end", texto + "\n")
                text_result.see("end")
                break
        else:
            text_result.insert("end", "Produto não encontrado.\n")
            text_result.see("end")
        entry_produto.delete(0, "end")
    except Exception:
        messagebox.showerror("Erro", "Erro ao buscar produto!")
# ---------------------------------------Configurações de personalização do CTK-----------------------------------------------------------------


def sair():
    if messagebox.askokcancel("Sair", "Deseja mesmo sair?"):
        janela.destroy()
# ------------------------------------------------------------------------------------------------------------------------------


def alterar_tema():
    tema = switch_tema.get()
    ctk.set_appearance_mode("Dark" if tema == "Escuro" else "Light")


# ------------------------------------------------------------------------------------------------------------------------------
janela = ctk.CTk()
janela.title("Mercado Olimpo")
janela.geometry("800x600")
# ------------------------------------------------------------------------------------------------------------------------------
frame_topo = ctk.CTkFrame(janela)
frame_topo.pack(pady=10, fill="x")
# ------------------------------------------------------------------------------------------------------------------------------
label_tema = ctk.CTkLabel(frame_topo, text="Tema:", font=("Arial", 13))
label_tema.pack(side="left", padx=10)
# ------------------------------------------------------------------------------------------------------------------------------
switch_tema = ctk.CTkOptionMenu(
    frame_topo, values=["Claro", "Escuro"], command=lambda e: alterar_tema())
switch_tema.set("Claro")
switch_tema.pack(side="left")
# ------------------------------------------------------------------------------------------------------------------------------
label_sessao = ctk.CTkLabel(
    janela, text="Selecione a sessão:", font=("Arial", 14))
label_sessao.pack(pady=5)
# ------------------------------------------------------------------------------------------------------------------------------
opcoes_sessao = list(sessao.keys())
var_sessao = ctk.StringVar(value=opcoes_sessao[0])
menu_sessao = ctk.CTkOptionMenu(
    janela, values=opcoes_sessao, variable=var_sessao, command=att_produto)
menu_sessao.pack(pady=5)
# ------------------------------------------------------------------------------------------------------------------------------
lista_produto = Listbox(janela, width=50, height=10)
lista_produto.pack(pady=5)
# ------------------------------------------------------------------------------------------------------------------------------
lista_carrinho = Listbox(janela, width=50, height=10)
lista_carrinho.pack(pady=5)
# ------------------------------------------------------------------------------------------------------------------------------
label_total = ctk.CTkLabel(janela, text="Total: R$ 0.00", font=("Arial", 14))
label_total.pack(pady=5)
carregar_carrinho()
# ------------------------------------------------------------------------------------------------------------------------------
label_codigo = ctk.CTkLabel(
    janela, text="Nome do produto:", font=("Arial", 14))
label_codigo.pack(pady=10)
# ------------------------------------------------------------------------------------------------------------------------------
entry_produto = ctk.CTkEntry(janela, width=200, font=("Arial", 13))
entry_produto.pack(pady=5)
# ------------------------------------------------------------------------------------------------------------------------------
frame_botoes = ctk.CTkFrame(janela)
frame_botoes.pack(pady=10)
# ------------------------------------------------------------------------------------------------------------------------------
btn_buscar = ctk.CTkButton(frame_botoes, text="Buscar Produto", command=buscar)
btn_buscar.grid(row=0, column=0, padx=10)

btn_add = ctk.CTkButton(
    frame_botoes, text="Adicionar ao Carrinho", command=add_carrinho)
btn_add.grid(row=0, column=1, padx=10)

btn_add = ctk.CTkButton(
    frame_botoes, text="Remover do Carrinho", command=remover_item)
btn_add.grid(row=0, column=2, padx=10)

btn_limpar = ctk.CTkButton(
    frame_botoes, text="Limpar Carrinho", command=limpar_carrinho)
btn_limpar.grid(row=1, column=0, padx=10)

btn_sair = ctk.CTkButton(frame_botoes, text="Sair", command=sair)
btn_sair.grid(row=0, column=3, padx=10)

btn_finalizar = ctk.CTkButton(
    frame_botoes, text="Finalizar compra", command=finalizar_compra)
btn_finalizar.grid(row=1, column=1, padx=10)

btn_historico = ctk.CTkButton(
    frame_botoes, text="Histórico", command=mostrar_historico)
btn_historico.grid(row=1, column=2, padx=10)

# ------------------------------------------------------------------------------------------------------------------------------
text_result = ctk.CTkTextbox(
    janela, width=550, height=250, font=("Consolas", 12))
text_result.pack(pady=10)
text_result.insert("end", "Bem-vindo ao Mercado Olimpo!\n\n")
# ------------------------------------------------------------------------------------------------------------------------------
att_produto(opcoes_sessao[0])
# ------------------------------------------------------------------------------------------------------------------------------
janela.protocol("WM_DELETE_WINDOW", sair)
janela.mainloop()
# ------------------------------------------------------------------------------------------------------------------------------
