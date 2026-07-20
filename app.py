from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)


# INICIA A CRIAÇÃO DO BANCO DE DADOS
def iniciar_banco():
    conexao = sqlite3.connect("banco.db")# Cria a conexão do SQlite com o arquivo a ser criado
    cursor = conexao.cursor()# Cria o Cursor para usar os comandos 

    # Comando para a criação da tabela USUARIOS
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               senha TEXT NOT NULL
               )""")

    conexao.commit()# Salva a alteração
    conexao.close()# Fecha a conexão com o db para não ter erro

iniciar_banco()# Inicia a criação do banco de dados ao rodar o script acima 

@app.route('/painel')
def tela_principal():
    return render_template('painel.html')

#Exibir página HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def tela_login():
    return render_template('login.html')

# Puxa a action do HTML
@app.route('/enviar-dados', methods = ['POST'])
def salvar_no_banco(): # Cria a função Salvar no banco de dados
    nome_usuario = request.form.get('nome') # Puxa o nome que o usuario digita no input do HTML usando o atributo name 'nome' que defini
    email_usuario = request.form.get('email') # Puxa o e-mail que o usuario digita no input do HTML usando o atributo name 'email' que defini
    senha_usuario = request.form.get('senha')

    conexao = sqlite3.connect('banco.db') # Cria a conexão do SQlite com o banco de dados
    cursor = conexao.cursor()# Cria o Cursor para usar os comandos 

    cursor.execute("INSERT INTO usuarios (nome,email,senha) VALUES (?,?,?)", (nome_usuario,email_usuario,senha_usuario,)) # Aqui uso o INSERT para pegar as informações que o usuario digitou e insiro no banco de dados

    conexao.commit() # Salva a alteração
    conexao.close()  # Fecha a conexão
        
    return redirect(url_for('tela_principal'))


@app.route('/login', methods = ['POST'])
def autenticar_usuario():
    email_login = request.form.get('email') # Aqui puxo o email que o usuario digitou no INPUT na parte de login
    senha_usuario = request.form.get('senha')

    conexao = sqlite3.connect('banco.db') # Cria a conexão do SQlite com o banco de dados
    cursor = conexao.cursor()# Cria o Cursor para usar os comandos 

    cursor.execute("""SELECT * FROM usuarios WHERE email = ? and senha = ?""", (email_login, senha_usuario)) # Aqui uso o SELECT para selecionar o nome e o email que a pessoa cadastrou na parte anterior,o nome_login e email_login serve para puxar o que o usuario digitou no campo nome e email
    usuario_encontrado = cursor.fetchone() # Crio essa variavel para poder ver se ela é ou não verdadeira 
    # O fetchone serve para "pescar" essa linha encontrada e a entrega para a sua variável usuario_encontrado

    conexao.close()

    # Estrutura de validação para Login
    if usuario_encontrado:
        return redirect(url_for('tela_principal'))
    else:
        return """
        <h2>Usúario não encontrado!</h2>
        <p>Ainda não tem uma conta? <a href="/">Clique aqui</a> </p>
        <p>Ou <a href="/login"> Tente fazer o Login novamente. </a></p>
"""

if __name__ == '__main__':
    app.run(debug=True)