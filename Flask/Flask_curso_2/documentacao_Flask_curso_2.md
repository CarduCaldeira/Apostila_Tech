# Flask: curso 2

Voltar à [Página inicial](../../README.md).

Neste markdown irei documentar o curso "Flask: avançando no desenvolvimento web com Python" da Alura enquanto realizo ele.

O projeto em que serão aplicados os conceitos estão nesta pasta Flask_curso_2. 

Para não nos perdemos entre as modificações no projeto e esta documentação, todo commmit dado será reportado aqui. A ideia é que tal documento siga o curso de forma linear.

## Preparando o ambiente

Versões utilizadas

- Python: 3.10.4
- Flask: 2.0.2
## Primeiros passos

Instale um ambiente virtual 
```
python3 -m venv ./venv
```
Para ativar 
```
source /home/carlos/Documentos/Apostila_Tech/Apostila_Tech/Flask/Flask_curso_2/venv/bin/activate
```
Para instalar os requirementos rode
```
pip3 install -r requirements.txt 
```

Aqui darei o primeiro commit com nome "primeiros passos para Flask: webapp".

## MySQL e SQLAlchemy no Flask

Primeiro para conseguirmos conectar nossa aplicação em Flask com o MySQL devemos instalar o mysql-connector-python. Para isso de o comando 
```
pip install mysql-connector-python==8.0.28
```
Vamos criar nosso banco de dados no MySQL. Para isso temos um arquivo **prepara.py** que irá criara o banco de dados e as nossas tabela.
```
import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='suasenha'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES['Jogos'] = ('''
      CREATE TABLE `jogos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Divino", "BD", "alohomora"),
      ("Camila Ferreira", "Mila", "paozinho"),
      ("Guilherme Louro", "Cake", "python_eh_vida")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from jogoteca.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
```
Após isso execute tal arquivo. Porém até o momento só criamos o banco de dados, agora devemos conectá-lo ao Flask (para isso usaremos o SQLAlchemy). Instale o SQLAlchemy com o comando
```
pip install flask-sqlalchemy==2.5.1
```
E em **jogotece.py** insira 
```
from flask_sqlalchemy import SQLAlchemy
```
para importar o SQLAlchemy. Para configurá-lo
```
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'suasenha',
        servidor = 'localhost',
        database = 'jogoteca'
    )

db = SQLAlchemy(app)
```
Crie as duas classes que irão corresponder às tabelas do banco de dados, a tabela Jogos e a de Usuarios
```
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
```
Agora podemos deletar as duas classes Jogo e Usuario e as instanciações de seus respectivos objetos, isto é, o código abaixo:
```
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }
```
Se rodarmos nossa aplicação nessse momento ela ira apresentar um erro, já que nossas rotas dependiam dos objetos instanciados nas duas classes que deletamos. Precisamos adaptar nosso código.
Na função **index** insira
```
lista = Jogos.query.order_by(Jogos.id)
```
Em http://127.0.0.1:5000/ já podemos visualizar a tabela com os jogos que inserimos na tabela do nosso banco de dados. 

## Inserindo dados no banco de dados

Anteriormente modificamos o código com o proposito de mostrar os jogos no banco de dados. Agora queremos inserir novos jogos no banco de dados. Antes de inserirmos propriamente novos jogos devemos alterar a rota **autenticar**, pois so usuarios logados devem ter permissão inserir novos jogos. Assim,
altere
```
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))

    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
```
para 
```
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
```
Uma vez que estejamos autenticados seremos direcionados para a pagina **novo.html**, onde informaremos
os dados do novo jogo (que serão enviados para a rota **criar**). Na rota **criar** altere
```
@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))
```
para
```
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo: #vemos se o jogo já nao esta cadastrado
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo) #salvando no banco de dados
    db.session.commit()       #salvando no banco de dados

    return redirect(url_for('index'))
```
## Reestruturando o código

Para deixar mais organizado nosso código iremos desmembrar o **jogoteca.py** em outros arquivos **.py**. Retire as classes models e coloque em um arquivo **models.py** da seguinte forma:
```
from jogoteca import db

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
```
Também crie um arquivo **views.py** e coloque as rotas nele. Neste arquivo voce deve importar
```
from flask import  render_template, request, redirect, flash, session, url_for
from jogoteca import app
```
Por último vamos criar um arquivo de configuração. Nele coloque
```
SECRET_KEY = 'teste'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '12345678',
        servidor = 'localhost',
        database = 'jogoteca'
    )
```
Assim, o **jogoteca.py** pode importar as configurações de **config.py**. Ao final o **jogoteca.py** deve ficar
```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)
```
## Editando o banco de dados

Já conseguimos visualizar e criar jogos, agora vamos inserir botões de editar e deletar os jogos.
Então crie os botões 
```
 <td>
    <a href="{{url_for('editar', id=jogo.id)}}" > Editar </a>
    <a href="{{ url_for('deletar', id=jogo.id) }}">Deletar</a>
 </td>
 ```
 Primeiro vamos fazer a rota editar (nela checaremos se o usuario esta logado e enviara o jogo a ser editado). 
```
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo)
```
Que ira direcionar para o **editar.html** caso esteja logado. O **editar.html** sera
```
{% extends "template.html" %}
{% block conteudo %}
<form action="{{ url_for('atualizar') }}" method="post">
  <fieldset>
    <input type="hidden" name="id" value="{{ jogo.id }}">
    <div class="form-group">
      <label for="nome">Nome</label>
      <input type="text" id="nome" name="nome" class="form-control"  value="{{ jogo.nome }}">
    </div>
    <div class="form-group">
      <label for="categoria">Categoria</label>
      <input type="text" id="categoria" name="categoria" class="form-control"  value="{{ jogo.categoria }}">
    </div>
    <div class="form-group">
      <label for="console">Console</label>
      <input type="text" id="console" name="console" class="form-control"  value="{{ jogo.console }}">
    </div>
    <button type="submit" class="btn btn-primary btn-salvar">Salvar</button>
  </fieldset>
</form>
{% endblock %}
```
Que por fim ira recolher as atualizaçoes no formulario e direcionar para atualizar que salvara no banco de dados
```
@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))
```
Para o botão deletar só faltar criar a rota do deletar
```
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))
```

## Lidando com imagens

A seguir vamos incorporar um campo no nosso formulário para receber imagens. Insira
```
<form action="{{ url_for('criar') }}" method="post" enctype="multipart/form-data">
  <input type="file" name ="arquivo" accept=".jpg"> 
```
no lugar de
```
<form action="{{ url_for('criar') }}" method="post">
```
Com o comando **accept=".jpg"** estamos restrigindo os arquivos para jpg. Agora, no metodo criar precisamos receber o arquivo e salvá-lo (no caso vamos salvar em uma pasta uploads). Assim, abaixo de 
```
db.session.commit()
```
insira
```
arquivo = request.files['arquivo']
upload_path = app.config['UPLOAD_PATH']
arquivo.save(f'{upload_path}/capa{novo_jogo.id}.jpg')
```
Nos códigos anteriores estamos referenciando uma configuração( que iremos salvar em **config.py** o caminho de onde salvaremos as imagens). Em **config.py** adicione 
```
import os

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__))+'/uploads'
```
O próximo passo é adicionar uma imagem padrão (caso o usuário não informe um imagem esta imagem padrao será adicionada) e além disso, no cadastro (na rota novo/) e ao editar mostraremos a imagem que esta salva daquele jogo. Adicione uma imagem como padrão em uploads como nome capa_padrao.jpg. Em **novo.html** adicone 
```
<figure class="img thumbnail col-md-4">
    <img class="img-fluid" src="{{ url_for('imagem', nome_arquivo='capa_padrao.jpg') }}">
    <figcaption>
      <label class="fileContainer">
        Mudar Capa
        <input type="file" name="arquivo" accept=".jpg">
      </label>
    </figcaption>
</figure>
```
no lugar de 
```
<input type="file" name="arquivo" accept=".jpg">
```
Note que estamos referenciando uma rota **imagem**, vamos implementá-la. Em **views.py** adicione
```
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
```
Devemos importar o send_from_directory. Porque estamos utilizando o **send_from_directory** se poderíamos informar diretamente a pasta que iremos pegar a imagem? Pois não é uma boa pratica informar explicitamente onde o arquivo está.

Se olharmos a rota novo agora note que a imagem está muito grande e seu visual não está bom, vamos estilizar isso com um arquivo css. Adicione um arquivo na pasta static com o nome app.css com o seguinte código
```
body {
    padding-top: 10px;
}

.btn {
    margin-bottom: 10px;
}

.container {
    border-radius: 4px;
    margin: auto;
    width: 80%;
}

.little-container {
    width: 40%;
    margin: auto;
}

figcaption {
    text-align: center;
    margin: 3px auto;
}

.fileContainer {
    overflow: hidden;
    position: relative;
}

.fileContainer [type=file] {
    cursor: pointer;
    display: block;
    font-size: 999px;
    filter: alpha(opacity=0);
    min-height: 100%;
    min-width: 100%;
    opacity: 0;
    position: absolute;
    right: 0;
    text-align: right;
    top: 0;
}

td {
    text-align: center;
}

.formularioJogo {
    display: flex;
}

.formularioImagem {
    margin-right: 16px
}

.buttons {
    margin-top: 16px
}

.inputBox {
    width: 700px;
}

.inputsJogo {
    width: 100%;
    margin-left: 1em;
    margin-bottom: 1em;
}
```
Insera o novo stylesheet de **app.css** no arquivo de **template.html**
```
<link rel="stylesheet" href="{{ url_for('static', filename='app.css') }}">
```
Podemos fazer o mesmo tratamento com imagem que foi feito com a rota **novo** com a rota **editar**(veja como fica no código).

Aqui darei um novo commit "tratamento de imagem".




