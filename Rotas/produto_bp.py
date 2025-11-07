from flask import render_template, request, redirect, Blueprint, send_from_directory, send_file, session
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
    if 'Usuario_Logado' not in session:
        return redirect('/login')

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

    id_usuario = session['id_usuario']

    cursor.execute(
        """
        INSERT INTO produto (nome, marca, preco, modelo, categoria, estoque, descricao, imagem, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nome, marca, preco, modelo, categoria, estoque, descricao, imagem_blob, id_usuario)
    )
    banco.commit()
    cursor.close()
    banco.close()

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
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    banco = ligar_banco()
    cursor = banco.cursor()
    id_usuario = session['id_usuario']

    cursor.execute("SELECT * FROM produto WHERE id_usuario = %s ORDER BY id_produto DESC", (id_usuario,))
    produtos = cursor.fetchall()
    cursor.close()
    banco.close()

    return render_template('meusProdutos.html', produtos=produtos, usuario=session)


@bp.route('/editarProduto/<int:id>', methods=['GET', 'POST'])
def editarProduto(id):
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    banco = ligar_banco()
    cursor = banco.cursor()

    # Verificar se o produto pertence ao usuário logado
    cursor.execute("SELECT id_usuario FROM produto WHERE id_produto=%s", (id,))
    produto = cursor.fetchone()

    # Se o produto não existe ou pertence a outro usuário, bloqueia o acesso
    if not produto or produto[0] != session['id_usuario']:
        cursor.close()
        banco.close()
        return redirect('/meusProdutos')

    #atualizar as informações
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        preco = float(request.form['preco'])
        modelo = request.form['modelo']
        categoria = request.form['categoria']
        estoque = int(request.form['estoque'])
        descricao = request.form['descricao']
        imagem = request.files['imagem-produto']
        imagem_blob = imagem.read()


        cursor.execute("""
                       UPDATE produto
                       SET nome=%s,
                           marca=%s,
                           preco=%s,
                           modelo=%s,
                           categoria=%s,
                           estoque=%s,
                           descricao=%s,
                           imagem=%s
                       WHERE id_produto = %s
                       """, (nome, marca, preco, modelo, categoria, estoque, descricao,imagem_blob,id))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect('/meusProdutos')

    # mostrar as informações no form
    cursor.execute("SELECT * FROM produto WHERE id_produto=%s AND id_usuario=%s", (id, session['id_usuario']))
    produto = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template('editarProduto.html', produto=produto)


@bp.route("/excluirProduto/<int:id>", methods=["GET"])
def excluirProduto(id):
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    banco = ligar_banco()
    cursor = banco.cursor()
    # Verificar se o produto pertence ao usuário antes de excluir
    cursor.execute("DELETE FROM produto WHERE id_produto=%s AND id_usuario=%s", (id, session['id_usuario']))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect("/meusProdutos")


# --------------HOME ----------------
@bp.route('/')
def home():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto ORDER BY RANDOM() LIMIT 4 ")
    produtosMaisVendidos = cursor.fetchall()

    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto ORDER BY RANDOM() LIMIT 4 ")
    produtosPromocoes = cursor.fetchall()

    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto ORDER BY RANDOM() LIMIT 4 ")
    produtosNovos = cursor.fetchall()

    cursor.close()
    banco.close()
    return render_template('index.html',
                           produtosNovos=produtosNovos,
                           produtosMaisVendidos=produtosMaisVendidos,
                           produtosPromocoes=produtosPromocoes)


# --------------HOME ----------------

# --------------PRODUTOS ----------------
@bp.route('/produtos')
def produtos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto ORDER BY RANDOM() ")
    produtosMaisVendidos = cursor.fetchall()

    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto ORDER BY RANDOM() ")
    produtosPromocoes = cursor.fetchall()

    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto ORDER BY RANDOM()")
    produtosNovos = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template('produtos.html',
                           produtosMaisVendidos=produtosMaisVendidos,
                           produtosPromocoes=produtosPromocoes,
                           produtosNovos=produtosNovos)


# --------------PRODUTOS ----------------

# --------------VER PRODUTO----------------
@bp.route('/verProduto/<id_produto>')
def verProduto(id_produto):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        "SELECT id_produto, nome,modelo, preco, imagem, descricao FROM produto WHERE id_produto = %s",
        (id_produto,)
    )
    produtos = cursor.fetchall()
    cursor.close()
    banco.close()
    produto = produtos[0] if produtos else None

    return render_template('verProduto.html', produto=produto)


# --------------VER PRODUTO----------------


# --------------CARRINHO----------------


@bp.route('/adicionar_carrinho/<int:id_produto>')
def adicionar_carrinho(id_produto):
    if 'Usuario_Logado' not in session:
        # Armazena a URL para redirecionar após login
        session['redirect_after_login'] = f'/adicionar_carrinho/{id_produto}'
        return redirect('/login')

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_produto, nome, preco, imagem FROM produto WHERE id_produto = %s", (id_produto,))
    produto = cursor.fetchone()
    cursor.close()
    banco.close()

    if not produto:
        return redirect('/')

    # Usa o ID do usuário como chave para o carrinho
    user_cart_key = f"carrinho_{session['id_usuario']}"

    if user_cart_key not in session:
        session[user_cart_key] = []

    carrinho = session[user_cart_key]

    # Verifica se o produto já está no carrinho
    for item in carrinho:
        if item['id'] == produto[0]:
            item['quantidade'] += 1
            break
    else:
        carrinho.append({
            'id': produto[0],
            'nome': produto[1],
            'preco': float(produto[2]),
            'imagem': f"/imagem/{produto[0]}",
            'quantidade': 1
        })

    session[user_cart_key] = carrinho
    session.modified = True

    return redirect('/carrinho')


@bp.route('/carrinho')
def carrinho():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    user_cart_key = f"carrinho_{session['id_usuario']}"
    carrinho = session.get(user_cart_key, [])
    total_itens = sum(item['quantidade'] for item in carrinho)
    total_valor = sum(item['preco'] * item['quantidade'] for item in carrinho)
    return render_template(
        'carrinho.html',
        carrinho=carrinho,
        total_itens=total_itens,
        total_valor=total_valor
    )

@bp.route('/remover_item/<int:id_produto>')
def remover_item(id_produto):
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    user_cart_key = f"carrinho_{session['id_usuario']}"
    carrinho = session.get(user_cart_key, [])
    carrinho = [item for item in carrinho if item['id'] != id_produto]
    session[user_cart_key] = carrinho
    session.modified = True
    return redirect('/carrinho')


@bp.route('/aumentar_quantidade/<int:id_produto>')
def aumentar_quantidade(id_produto):
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    user_cart_key = f"carrinho_{session['id_usuario']}"
    if user_cart_key in session:
        carrinho = session[user_cart_key]
        for item in carrinho:
            if item['id'] == id_produto:
                item['quantidade'] += 1
                break
        session[user_cart_key] = carrinho
        session.modified = True
    return redirect('/carrinho')


@bp.route('/diminuir_quantidade/<int:id_produto>')
def diminuir_quantidade(id_produto):
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    user_cart_key = f"carrinho_{session['id_usuario']}"
    if user_cart_key in session:
        carrinho = session[user_cart_key]
        for item in carrinho:
            if item['id'] == id_produto:
                if item['quantidade'] > 1:
                    item['quantidade'] -= 1
                break
        session[user_cart_key] = carrinho
        session.modified = True
    return redirect('/carrinho')

# --------------CARRINHO----------------

# --------------PAGAMENTO----------------
@bp.route('/pagamento')
def pagamento():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    carrinho = session.get('carrinho', [])

    # Evita erro se o carrinho estiver vazio
    total_itens = sum(item['quantidade'] for item in carrinho) if carrinho else 0
    total_valor = sum(item['preco'] * item['quantidade'] for item in carrinho) if carrinho else 0

    return render_template(
        'pagamento.html',
        carrinho=carrinho,
        total_itens=total_itens,
        total_valor=total_valor
    )


# --------------PAGAMENTO----------------


# --------------ENTREGA----------------
@bp.route('/entrega')
def entrega():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    carrinho = session.get('carrinho', [])

    total_itens = sum(item['quantidade'] for item in carrinho) if carrinho else 0
    total_valor = sum(item['preco'] * item['quantidade'] for item in carrinho) if carrinho else 0

    return render_template(
        'entrega.html',
        carrinho=carrinho,
        total_itens=total_itens,
        total_valor=total_valor
    )


# --------------ENTREGA----------------


# --------------CONFRMAÇÃO DO PAGAMENTO----------------
@bp.route('/confirmacaoPagamento')
def confirmacao_pagamento():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    carrinho = session.get('carrinho', [])
    total_itens = sum(item['quantidade'] for item in carrinho) if carrinho else 0
    total_valor = sum(item['preco'] * item['quantidade'] for item in carrinho) if carrinho else 0

    session['carrinho'] = []

    return render_template(
        'confirmacaoPagamento.html',
        total_itens=total_itens,
        total_valor=total_valor
    )


# --------------CONFRMAÇÃO DO PAGAMENTO----------------


# --------------FAVORITOS----------------

@bp.route('/favoritos')
def favoritos():
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    banco = ligar_banco()
    cursor = banco.cursor()

    id_usuario = session['id_usuario']

    cursor.execute("""
                   SELECT p.id_produto, p.nome, p.preco, p.imagem
                   FROM favoritos f
                            INNER JOIN produto p ON f.id_produto = p.id_produto
                   WHERE f.id_usuario = %s
                   ORDER BY f.id_favorito DESC
                   """, (id_usuario,))
    favoritos = cursor.fetchall()

    cursor.close()
    banco.close()

    return render_template('favoritos.html', favoritos=favoritos)


@bp.route('/adicionar_favorito/<int:id_produto>')
def adicionar_favorito(id_produto):
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    banco = ligar_banco()
    cursor = banco.cursor()
    id_usuario = session['id_usuario']

    # Verifica se o produto já está nos favoritos
    cursor.execute("""
                   SELECT 1
                   FROM favoritos
                   WHERE id_usuario = %s
                     AND id_produto = %s
                   """, (id_usuario, id_produto))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
                       INSERT INTO favoritos (id_usuario, id_produto)
                       VALUES (%s, %s)
                       """, (id_usuario, id_produto))
        banco.commit()

    cursor.close()
    banco.close()
    return redirect('/favoritos')


@bp.route('/remover_favorito/<int:id_produto>')
def remover_favorito(id_produto):
    if 'Usuario_Logado' not in session:
        return redirect('/login')

    banco = ligar_banco()
    cursor = banco.cursor()
    id_usuario = session['id_usuario']

    cursor.execute("""
                   DELETE
                   FROM favoritos
                   WHERE id_usuario = %s
                     AND id_produto = %s
                   """, (id_usuario, id_produto))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/favoritos')

# --------------FAVORITOS----------------
