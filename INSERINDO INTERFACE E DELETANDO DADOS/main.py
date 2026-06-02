from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error, IntegrityError

app = Flask(__name__)
app.secret_key = "chave_secreta_para_alertas_flash"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Adicione sua senha do MySQL aqui
    'database': 'sistema_clientes'
}


def obter_conexao_banco():
    """Retorna uma conexão ativa com o banco de dados MySQL."""
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    return None


@app.route('/')
def index():
    """Rota principal que exibe o formulário de cadastro e a tabela de clientes cadastrados."""
    clientes = []
    conexao = obter_conexao_banco()

    if conexao:
        cursor = None
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT cpf, nome, email, telefone FROM clientes")
            clientes = cursor.fetchall()
        except Error as e:
            flash(f"Erro ao buscar clientes no banco de dados: {e}", "erro")
        finally:
            if cursor is not None:
                cursor.close()
            if conexao.is_connected():
                conexao.close()
    else:
        flash("Não foi possível conectar ao banco de dados MySQL local. Verifique as configurações.", "erro")

    return render_template('index.html', clientes=clientes)


@app.route('/cadastrar', methods=['POST'])
def cadastrar_cliente():
    """Rota responsável por processar o envio do formulário e salvar o cliente no MySQL."""
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    cpf_limpo = ''.join(filter(str.isdigit, cpf)) if cpf else ''
    if not nome or not cpf_limpo or not email:
        flash("Nome, CPF e E-mail são campos obrigatórios!", "erro")
        return redirect(url_for('index'))

    conexao = obter_conexao_banco()
    if conexao:
        cursor = None
        try:
            cursor = conexao.cursor()
            comando_sql = "INSERT INTO clientes (cpf, nome, email, telefone) VALUES (%s, %s, %s, %s)"
            dados_cliente = (cpf_limpo, nome, email, telefone)
            cursor.execute(comando_sql, dados_cliente)
            conexao.commit()
            flash("Cliente cadastrado com sucesso!", "sucesso")
        except IntegrityError:
            flash("Erro: Já existe um cliente cadastrado com este CPF!", "erro")
        except Error as e:
            flash(f"Erro ao inserir no banco de dados: {e}", "erro")
        finally:
            if cursor is not None:
                cursor.close()
            if conexao.is_connected():
                conexao.close()
    else:
        flash("Banco de dados offline. Cadastro não realizado.", "erro")

    return redirect(url_for('index'))


@app.route('/excluir/<cpf>', methods=['POST'])
def excluir_cliente(cpf):
    """Rota para deletar com segurança um cliente utilizando o CPF como identificador exclusivo."""
    conexao = obter_conexao_banco()

    if conexao:
        cursor = None
        try:
            cursor = conexao.cursor()
            comando_sql = "DELETE FROM clientes WHERE cpf = %s"
            cursor.execute(comando_sql, (cpf,))
            conexao.commit()
            flash("Cliente removido com sucesso!", "sucesso")
        except Error as e:
            flash(f"Erro ao excluir cliente: {e}", "erro")
        finally:
            if cursor is not None:
                cursor.close()
            if conexao.is_connected():
                conexao.close()
    else:
        flash("Banco de dados offline. Não foi possível realizar a exclusão.", "erro")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
