from flask import render_template, request, redirect,Blueprint,session
import psycopg2

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="HardMarket",
        user="postgres",
        password="senai",
    )
    return banco

bp = Blueprint('usuario_bp', __name__)



@bp.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    # Captura todos os dados enviados pelo formulário
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']
    data_nascimento = request.form['data_nascimento']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cep = request.form['cep']
    rua = request.form['rua']
    bairro = request.form['bairro']
    numero = request.form['numero']
    banco = ligar_banco()
    cursor = banco.cursor()
    # Insere o novo usuário na tabela
    cursor.execute(
        """
        INSERT INTO usuario (nome, email, senha, telefone, data_nascimento, cidade, estado, cep, rua, bairro, numero)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nome, email, senha, telefone, data_nascimento, cidade, estado, cep, rua, bairro, numero)
    )
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/login')


