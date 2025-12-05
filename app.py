from flask import Flask, render_template, request, redirect, session
from Rotas import usuario_bp, produto_bp
import psycopg2


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="HardMarket",
        user="postgres",
        password="senai",
    )
    return banco


app = Flask(__name__)

app.secret_key = "HardSenhaSegura"

app.register_blueprint(usuario_bp.bp)
app.register_blueprint(produto_bp.bp)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/produtos')
def produtos():
    return render_template('produtos.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/confirmacaoPagamento')
def confirmacaoPagamento():
    return render_template('confirmacaoPagamento.html')


@app.route('/entrega')
def entrega():
    return render_template('entrega.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/favoritos')
def favoritos():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    return render_template('favoritos.html')


@app.route('/login')
def login():
    # Se o usuário já estiver logado, redireciona direto
    if 'Usuario_Logado' in session:
        return redirect('/usuarioLogado')
    return render_template('login.html')


@app.route('/meusProdutos')
def meusProdutos():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    return render_template('meusProdutos.html')


@app.route('/pagamento')
def pagamento():
    return render_template('pagamento.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/vender')
def vender():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    return render_template('vender.html')


@app.route('/verProduto')
def verProduto():
    return render_template('verProduto.html')


# -----------LOGIN--------------

@app.route('/autenticar', methods=["POST"])
def autenticar():
    email = request.form['email']
    senha = request.form['senha']

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_usuario, nome FROM usuario WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    banco.close()

    if usuario:
        session['Usuario_Logado'] = True
        session['id_usuario'] = usuario[0]
        session['nome_usuario'] = usuario[1]
        session['email'] = email
        return redirect('/')
    else:
        # Envia uma mensagem para o template
        erro = "E-mail ou senha incorretos"
        return render_template('login.html', erro=erro)


@app.route('/deslogar')
def deslogar():
    session.clear()
    return redirect('/login')


# -----------LOGIN--------------

@app.route('/usuarioLogado')
def usuarioLogado():
    return render_template('usuarioLogado.html')


if __name__ == '__main__':
    app.run()
