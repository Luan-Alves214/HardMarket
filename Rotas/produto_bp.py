from flask import render_template, request, redirect, Blueprint, send_from_directory, send_file, url_for
import psycopg2
import io


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="HardMarket",
        user="postgres",
        password="senai",
    )
    return banco


bp = Blueprint('produto_bp', __name__)


@bp.route('/salvarProduto', methods=['POST'])
def salvarProduto():
    banco = ligar_banco()
    cursor = banco.cursor()
    nome = request.form['nome']
    marca = request.form['marca']
    preco = float(request.form['preco'])
    modelo = request.form['modelo']
    categoria = request.form['categoria']
    estoque = int(request.form['estoque'])
    descricao = request.form['descricao']
    imagem = request.files['imagem']
    imagem_blob = imagem.read()
    cursor.execute(
        """
        INSERT INTO produto (nome, marca, preco, modelo, categoria, estoque, descricao, imagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nome, marca, preco, modelo, categoria, estoque, descricao, imagem_blob)
    )
    banco.commit()

    return redirect('/meusProdutos')


def recuperar_foto(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT imagem FROM produto WHERE id_produto=%s', (id,))
    imagem_blob = cursor.fetchone()
    return imagem_blob[0]


@bp.route('/imagem/<id>')
def imagem(id):
    foto_blob = recuperar_foto(id)
    if foto_blob:
        return send_file(
            io.BytesIO(foto_blob),
            mimetype='image/jpeg',
            download_name=f'imagem_{id}.jpg'
        )
    else:
        return send_from_directory('static/imagens/', 'logo.png')


@bp.route('/meusProdutos', methods=['GET'])
def mostrarProdutos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        "SELECT * FROM produto ORDER BY id_produto DESC")
    produtos = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template('meusProdutos.html', produtos=produtos)


@bp.route('/editarProduto/<int:id>', methods=['GET', 'POST'])
def editarProduto(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        preco = float(request.form['preco'])
        modelo = request.form['modelo']
        categoria = request.form['categoria']
        estoque = int(request.form['estoque'])
        descricao = request.form['descricao']
        cursor.execute("""
                       UPDATE produto
                       SET nome=%s,
                           marca=%s,
                           preco=%s,
                           modelo=%s,
                           categoria=%s,
                           estoque=%s,
                           descricao=%s
                       WHERE id_produto = %s
                       """, (nome, marca, preco, modelo, categoria, estoque, descricao, id))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect('/meusProdutos')
    cursor.execute("SELECT * FROM produto WHERE id_produto=%s", (id,))
    produto = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template('editarProduto.html', produto=produto)


@bp.route("/excluirProduto/<int:id>", methods=["GET"])
def excluirProduto(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM produto WHERE id_produto=%s", (id,))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect("/meusProdutos")


