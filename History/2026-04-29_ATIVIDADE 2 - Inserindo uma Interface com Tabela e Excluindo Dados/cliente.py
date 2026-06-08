# import do flask para criação do servidor #render_template para criar uma "ponte" com html #request para capturar os dados digitados
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# "Ajuda" o Flask a localizar os caminhos dos arquivos
app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "escola",
    "database": "cadastro",
}


# Criando a rota para acessar o arquivo HTML
@app.route("/")
def index():
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()

        cursor.close()
        conexao.close()

        return render_template("index.html", clientes=clientes)

    except mysql.connector.Error as err:
        return f"Erro ao buscar clientes: {err}"


# Criem uma rota para acessar o formulario
@app.route("/cadastrar", methods=["post"])
def cadastrar():
    cpf = request.form["cpf"]
    primeiro_nome = request.form["primeiro_nome"]
    sobrenome = request.form["sobrenome"]
    idade = request.form["idade"]

    try:
        # Conectando ao banco de dados
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        # Inserindo os dados no banco
        sql = "INSERT INTO cliente (cpf, primeiro_nome, sobrenome, idade) VALUES (%s, %s, %s, %s)"
        valores = (cpf, primeiro_nome, sobrenome, idade)

        cursor.execute(sql, valores)
        conexao.commit()

        # Fechando a conexão
        cursor.close()
        conexao.close()

        print("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("index"))

    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar: {erro}", "error")
        return redirect(url_for("index"))


# Criem uma rota para deletar o cliente
@app.route("/deletar", methods=["post"])
def deletar():
    cpf = request.form["cpf"]
    try:
        # Conectando ao banco de dados
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        # Inserindo os dados no banco
        sql = "DELETE FROM cliente WHERE cpf = %s"
        valores = (cpf,)

        cursor.execute(sql, valores)
        conexao.commit()

        # Fechando a conexão
        cursor.close()
        conexao.close()

        print("Cliente deletado com sucesso!", "success")
        return redirect(url_for("index"))

    except mysql.connector.Error as erro:
        print(f"Erro ao deletar: {erro}", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
