from tkinter import *
from tkinter import messagebox
from pathlib import Path
import tkinter
import psycopg
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row

load_dotenv()

CAMINHO_IMAGENS = Path("janela")

# integração com banco de dados
conexao = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    row_factory=dict_row,
)

cursor = conexao.cursor()


# PROCURAR INSUMO
def btn_clicked0():
    # pegar a informação do campo nome_insumo (entry1)
    nome_insumo = entry1.get()
    # buscar essa informação do insumo no banco de dados
    # colocar no entryo (caixa de texto) as informações do insumo no banco de dados
    comando = """
        SELECT * FROM Insumos
        WHERE nome_insumo = %s
    """
    cursor.execute(comando, (nome_insumo,))
    entry0.delete("1.0", END)

    linha = cursor.fetchone()
    if linha is not None:
        texto = (
            f"Item: {linha['nome_insumo']}\n"
            f"Quantidade: {linha['qtde']}\n"
            f"Lote: {linha['lote']}\n"
            f"Validade: {linha['data_validade']}"
        )

        entry0.insert("1.0", texto)

    else:
        tkinter.messagebox.showinfo(
            title="Erro",
            message=f"{nome_insumo} não encontrado no bando de dados",
        )
    print("Procurar Insumo")


# DELETAR INSUMO
def btn_clicked1():
    # pegar a informação do campo nome_insumo (entry1)
    nome_insumo = entry1.get()
    # buscar e deletar a informação do insumo do banco de dados
    # exibir uma mensagem dizzendo que deletoy o insumo do banco de dados
    comando = """
        DELETE FROM Insumos
        WHERE nome_insumo = %s
    """

    cursor.execute(comando, (nome_insumo,))

    if cursor.rowcount == 0:
        tkinter.messagebox.showinfo(title="Erro", message="Insumo não encontrado")

    else:
        conexao.commit()
        tkinter.messagebox.showinfo(
            title="Aviso Insumo Excluido",
            message=f"{nome_insumo} foi excluido do banco de dados",
        )
        print("Deletar Insumo")


# REGISTRAR USO INSUMO
def btn_clicked2():
    # pegar a informação do campo nome_insumo (entry1)
    nome_insumo = entry1.get()
    qtde_usada = entry4.get()
    # pegar a informação do campo qtde (entry4)
    # buscar o insumo pelo nome dele no banco de dados
    # diminuir da quantidade do insumo a quantidade eu consumi
    comando = """
        UPDATE Insumos
        SET qtde = qtde - %s
        WHERE nome_insumo = %s
            AND qtde >= %s
        """

    cursor.execute(comando, (qtde_usada, nome_insumo, qtde_usada))

    # exibir uma mensagem dizendo quantas unidades eu consumi do banco de dados

    if cursor.rowcount == 0:
        conexao.rollback()
        tkinter.messagebox.showinfo(
            title="Erro", message="Quantidade insuficiente ou insumo não encontrado"
        )
    else:
        conexao.commit()
        tkinter.messagebox.showinfo(
            title="Aviso uso do insumo",
            message=f"{qtde_usada} unidades do {nome_insumo} foram consumidas",
        )
        print("Registrar Uso Insumo")


# ADICIONAR INSUMO
def btn_clicked3():
    # pegar todos os campos
    nome_insumo = entry1.get()
    data_validade = entry2.get()
    lote = entry3.get()
    qtde = entry4.get()
    # adicionar no banco de dados aquele insumo

    comando = """
        INSERT INTO Insumos(nome_insumo, data_validade, lote, qtde)
        VALUES (%s, %s, %s, %s)

        ON CONFLICT (nome_insumo, lote)
        DO UPDATE SET
        qtde = insumos.qtde + EXCLUDED.qtde;
    """

    cursor.execute(comando, (nome_insumo, data_validade, lote, qtde))
    conexao.commit()
    tkinter.messagebox.showinfo(
        title="Aviso Adicionar Produto", message="Produto Adicionado com Sucesso"
    )
    print("Adicionar insumo")


# print(entry1.get()) -> nome_insumo
# print(entry2.get()) -> data_validade
# print(entry3.get()) -> lote
# print(entry4.get()) -> quantidade
# entry0.get('1.0', END) -> campo para exibir o produto do banco de dados

window = Tk()

window.geometry("711x646")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=646,
    width=711,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.place(x=0, y=0)

background_img = PhotoImage(file=CAMINHO_IMAGENS / "background.png")
background = canvas.create_image(355.5, 323.0, image=background_img)

img0 = PhotoImage(file=CAMINHO_IMAGENS / "img0.png")
b0 = Button(
    image=img0, borderwidth=0, highlightthickness=0, command=btn_clicked0, relief="flat"
)

b0.place(x=479, y=195, width=178, height=38)

img1 = PhotoImage(file=CAMINHO_IMAGENS / "img1.png")
b1 = Button(
    image=img1, borderwidth=0, highlightthickness=0, command=btn_clicked1, relief="flat"
)

b1.place(x=247, y=197, width=178, height=36)

img2 = PhotoImage(file=CAMINHO_IMAGENS / "img2.png")
b2 = Button(
    image=img2, borderwidth=0, highlightthickness=0, command=btn_clicked2, relief="flat"
)

b2.place(x=479, y=123, width=178, height=35)

img3 = PhotoImage(file=CAMINHO_IMAGENS / "img3.png")
b3 = Button(
    image=img3, borderwidth=0, highlightthickness=0, command=btn_clicked3, relief="flat"
)

b3.place(x=247, y=125, width=178, height=34)

entry0_img = PhotoImage(file=CAMINHO_IMAGENS / "img_textBox0.png")
entry0_bg = canvas.create_image(455.0, 560.0, image=entry0_img)

entry0 = Text(bd=0, bg="#ffffff", highlightthickness=0)

entry0.place(x=250, y=502, width=410, height=114)

entry1_img = PhotoImage(file=CAMINHO_IMAGENS / "img_textBox1.png")
entry1_bg = canvas.create_image(517.0, 294.5, image=entry1_img)

entry1 = Entry(bd=0, bg="#ffffff", highlightthickness=0)

entry1.place(x=377, y=278, width=280, height=31)

entry2_img = PhotoImage(file=CAMINHO_IMAGENS / "img_textBox2.png")
entry2_bg = canvas.create_image(517.0, 340.5, image=entry2_img)

entry2 = Entry(bd=0, bg="#ffffff", highlightthickness=0)

entry2.place(x=377, y=324, width=280, height=31)

entry3_img = PhotoImage(file=CAMINHO_IMAGENS / "img_textBox3.png")
entry3_bg = canvas.create_image(517.0, 388.5, image=entry3_img)

entry3 = Entry(bd=0, bg="#ffffff", highlightthickness=0)

entry3.place(x=377, y=372, width=280, height=31)

entry4_img = PhotoImage(file=CAMINHO_IMAGENS / "img_textBox4.png")
entry4_bg = canvas.create_image(517.0, 436.5, image=entry4_img)

entry4 = Entry(bd=0, bg="#ffffff", highlightthickness=0)

entry4.place(x=377, y=420, width=280, height=31)

window.resizable(False, False)
window.mainloop()
