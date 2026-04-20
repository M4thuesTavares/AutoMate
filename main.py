from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from envia_email import disparar_email

app = Flask(__name__)

DIAS = 7

def get_db_connection():
    return sqlite3.connect('automate.db')

def dadosInicial():
    conn = get_db_connection()

    query = ("""SELECT Codigo, Descricao, DataUltimaManutecao ,DataProxManutecao FROM ONIBUS""")

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.to_dict(orient='records')

"""dados_rel = dadosInicial()
disparar_email(dados_rel)"""


def proxManutecoes():
    conn = get_db_connection()

    query = ("SELECT Codigo, Descricao, DataUltimaManutecao, DataProxManutecao FROM ONIBUS WHERE DataProxManutecao BETWEEN DATETIME('now') AND DATETIME('now',?)")

    param = f"+{DIAS} days"
    df = pd.read_sql_query(query, conn, params=(param,))

    return df.to_dict(orient='records') if not df.empty else []

def manutecoesAtrasada():
    conn = get_db_connection()

    query = ("SELECT Codigo, Descricao, DataUltimaManutecao, DataProxManutecao FROM ONIBUS WHERE DataProxManutecao < DATETIME('now')")

    df = pd.read_sql_query(query, conn)

    return df.to_dict(orient='records') if not df.empty else []

@app.route('/')
def home():

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()

    query =f"""SELECT Codigo, Descricao, DataUltimaManutecao, DataProxManutecao FROM ONIBUS LIMIT {per_page} OFFSET {offset}"""
    df = pd.read_sql_query(query, conn)

    total_onibus = conn.execute('SELECT COUNT(*) FROM ONIBUS').fetchone()[0]
    conn.close()

    dados = df.to_dict(orient='records')

    has_next = total_onibus > (page * per_page)
    has_prev = page > 1

    return render_template("index.html",dados=dados,page=page,has_next=has_next,has_prev=has_prev)

@app.route('/buscarProx')
def buscarProx():
    dados = proxManutecoes()

    return render_template("proxManutecao.html",dados=dados)

@app.route('/buscarAtras')
def buscarAtras():
    dados = manutecoesAtrasada()

    return render_template("manutecaoAtrasada.html",dados=dados)

app.run(debug=True)
