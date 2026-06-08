from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "escola",
    "database": "cadastro",
}


@app.route("/")
def index():
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            "SELECT `ID`, `PRODUTO`, `CATEGORIA`, `PRECO`, `ESTOQUEcliente` FROM `produtos`"
        )
        produtos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return render_template("index2.html", produtos=produtos)

    except mysql.connector.Error as err:
        return f"Erro ao buscar produtos: {err}"


@app.route("/cadastrar", methods=["post"])
def cadastrar():
    produto = request.form["produto"]
    categoria = request.form["categoria"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]

    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        sql = "INSERT INTO produtos (PRODUTO, CATEGORIA, PRECO, ESTOQUEcliente) VALUES (%s, %s, %s, %s)"
        valores = (produto, categoria, preco, estoque)

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        print("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("index"))

    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar: {erro}", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
