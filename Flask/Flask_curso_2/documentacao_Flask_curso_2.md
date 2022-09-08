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

## Um pouco de javascript

Note que quando selecionamos uma imagem ela não altera logo em seguida gostariamos que nossa pagina tivesse tal comprtamento. Para isso  vamos usar javascript. Cire um arquivo **app.js** em static e insira
```
$('form input[type="file"]').change(event => {
  let arquivos = event.target.files;
  if (arquivos.length === 0) {
    console.log('sem imagem pra mostrar')
  } else {
      if(arquivos[0].type == 'image/jpeg') {
        $('img').remove();
        let imagem = $('<img class="img-fluid">');
        imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
        $('figure').prepend(imagem);
      } else {
        alert('Formato não suportado')
      }
  }
});
```
Crie um novo arquivo chamado **jquery.js** e dentro da pasta static e inserir o código do JQuery versão 3.6.0.

Por fim adicione em template(por padrão adicionamos no fim do body)
```
<script type="text/javascript" src="{{ url_for('static', filename='jquery.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static', filename='app.js') }}"></script>
```

## Contornando o Cache

Temos um  problema em relação ao nosso código. Estamos atualizando as imagens sempre com o mesmo nome,
isso pode gerar problemas em relação ao cache. Como o nome não é alterado o cache pode não atualizar, logo mesmo que mudemos a imagem, como a pagina esta consultando o cache( que não foi atualizado) ela não ira mostrar a nossa imagem. Para corrigir isso crie um arquivo **helpers.py**
```
import os
from jogoteca import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):#os.listdir serve para listar os arquivos daquela pasta 
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
```

Primeiro a função **recupera_imagem** sera para pegar a imagem desejada e além disso temos que criar também a função
**deleta_arquivo** (como queremos salvar as imagens com nome distintos temos que excluir a imagem antiga). Note também que estamos usando o comando **os.path.join(app.config['UPLOAD_PATH'], arquivo))** que ira concatenar o caminho(novamente, é melhor informar o caminho dinamicamente, por exemplo se tivessemos o caminho projeto/uploads/capa1.png não daria certo no windows).

Em **views.py** deixe a rota editar da seguinte forma 
```
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)
```
E em **editar.html**  troque a variavel **nome_arquivo** para **capa_jogo**
```
<img class="img-fluid" src="{{ url_for('imagem', nome_arquivo=capa_jogo) }}">
```
E agora atualize o metodo **atualizar**
```
@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))
```
Também devemos implementar o mesmo padrão de nome de imagem(que será determinado pela hora exata de upload da imagem) no metodo criar
```
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))
```
Por ultimo importe os arquivos
```
from helpers import recupera_imagem, deleta_arquivo
import time
```

## Adiconando botoes

Vamos inserir botões em lista.html para conectar as rotas de novo, logout e login. Insira
```
<a class="btn btn-primary" href="{{ url_for('login') }}">Login</a>
<a class="btn btn-danger" href="{{ url_for('logout') }}">Logout</a>
<a class="btn btn-primary" href="{{ url_for('novo') }}">Novo Jogo</a> 
```
e abaixo de 
```
<button type="submit" class="btn btn-primary btn-salvar">Salvar</button>
```
insira
```
<a class="btn btn-danger" href="{{ url_for('index') }}">Voltar</a>
```

## Validação 
Queremos fazer uma validação dos jogos adicionados. O proprio Flask possui um pacote que nos ajudara a fazer isto (além de melhorar nossa segurança) .
Adicione em **jogoteca.py**
```
from flask_wtf.csrf import CSRFProtect
```
E no bash de 
```
pip install flask-wtf==1.0.0
```
Para instanciar a proteção contra CSRF no arquivo **jogoteca.py**
```
csrf = CSRFProtect(app)
```
Para podermos utilizar um formulário do Flask WTF, precisamos criar uma classe que vai representar esse formulário bem parecido com o que fizemos com o SQL Alchemy.
Faça o import do FlaskForm e demais bibliotecas necessárias do wtforms no **helpers.py**
```
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
```
E também adicione as seguintes classes no **helpers.py**
```
class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')
```
Em **views.py** importe as classes **FormularioJogo, FormularioUsuario**. E insira o comando
```
form = FormularioJogo()
```
acima do render_template e no render_template envie como paramentro o form com nome form.
Com isso precisamos alterar o formulario em **novo.html**, **editar** e **login.html**. Em **novo.html** altere
```
<label for="nome">Nome</label>
<input type="text" id="nome" name="nome" class="form-control">
```
por
```
{{ form.nome.label(class="form-label") }}
{{ form.nome(class="form-control") }}
```
Faça o mesmo para os campos categoria e console. Também troque o botão 
```
<button type="submit" class="btn btn-primary btn-salvar">Salvar</button>
```
por
```
{{ form.salvar(class="btn btn-primary") }}
```
Como os dados do formulario são enviados para o metodo criar então precisamos alterar ele também. Adicione em **criar**
form = FormularioJogo(request.form)
```
if not form.validate_on_submit():
    return redirect(url_for('novo'))
```
A grande vantagem de usar o wtforms é que quando validamos so aplicamos um if, ao invés de varios, assim, deixamos o código mais limpo. Para o wtforms não usamos o comando request.form, por isso troque eles por 
```
nome = form.nome.data
categoria = form.categoria.data
console = form.console.data
```
Com isso validamos o formulario para criar um novo jogo. Iremos fazer o mesmo com o formulário editar (com algumas diferenças já que no formulário editar já queremos sugerir os nomes salvos dentro do formulário). Assim, em **editar.html**
adicione 
```
form = FormularioJogo()
form.nome.data = jogo.nome
form.categoria.data = jogo.categoria
form.console.data = jogo.console
```
e no render_template mande como paramentro o form. Agora em **editar.html** faça o mesmo que foi feito
como o **novo.html** e substitua os labels e inputs.

Note agora que só estamos usando o **jogo.id** nesse formulário (sem precisar dos outros atributos do do objeto jogo, já que agora estamos usando os atributos do form), assim ao invés de passar o jogo no render template podemos so passor o id.

Dando prosseguimento a nossa validação em formulário insira em **atualizar** o comando no inicio do metodo
```
form = FormularioJogo(request.form)
```
Queremos que caso a validação seja True a atualização tenha prosseguimento eno final sejamos redirecionados para a página principal, caso contrário devemos ser apenas redirecionados
para a página principal. Assim o metodo autenticar fica
```
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))
```
Por último vamos fazer a validação do login. Como já criamos a classe **FormularioUsuario** em **helpers.py**, em **login** no **views.py** adicione 
```
form = FormularioJogo()
```
e envie pelo render_template o objeto form. Agora em **login.html**  troque 
```
<p><label>Nome de usuário:</label> <input class="form-control" type="text" name="usuario" required></p>
<p><label>Senha:</label> <input class="form-control" type="password" name="senha" required></p>
<p><button class="btn btn-primary" type="submit">Entrar</button></p>
```
por 
```
<div class="form-group">
    {{ form.nickname.label(class="form-label") }}
    {{ form.nickname(class="form-control") }}
</div>
<div class="form-group">
    {{ form.senha.label(class="form-label") }}
    {{ form.senha(class="form-control") }}
</div>
<div class="form-group">
    {{ form.login(class="btn btn-primary") }}
    <a class="btn btn-danger" href="{{ url_for('index') }}">Voltar</a>
</div>
```  
Por último em **autenticar** adicione
```
form = FormularioUsuario(request.form)
```
e troque 
```
request.form['usuario'] 
```
por 
```
form.nickname.data
```
Também 
```
request.form['senha']
```
por
```
form.senha.data
```                             
## CRSF token

O Cross-Site Request Forgery ou CSRF é uma vulnerabilidade na segurança da web que possibilita a um indivíduo mal intencionado se passar por um usuário inocente. Assim, a ameaça pode se disfarçar como o servidor e passar informações através do método POST.

Uma maneira mais prática de entender isso é através de um exemplo:
```
    Lucas está trabalhando em seu computador e se dá conta de que precisa transferir dinheiro de sua conta no banco. Ele passa por todo o processo de autenticação de usuário, acessa a sua conta no banco e faz a transferência necessária.

    Em seguida, se lembra de que deve checar seus e-mails e acessa um e-mail de origem duvidosa, que aparentemente não o leva a lugar nenhum.

    Contudo, poucos minutos depois ele recebe uma notificação o informando que uma quantia exorbitante foi transferida de sua conta. Lucas havia sido roubado por um hacker mal intencionado através do uso do CSRF.
```
Vamos analisar o ocorrido passo a passo: primeiramente, Lucas acessa sua conta no banco e faz a transferência que precisa. Ao realizar essa ação, o navegador dele cria um session token que caracteriza seu acesso autenticado ao banco.

Depois Lucas acessa o e-mail de origem duvidosa. Esse e-mail, enviado pelo hacker, possui um link que, ao simples acesso, permite utilizar o session token de Lucas. Dessa forma, é preenchido um formulário com informações de transferência bancária e o session token é usado para autenticá-lo e permitir que o método POST ocorra sem mais problemas.

A situação caracteriza a falta do uso do CSRF e aconteceu porque o servidor do banco não possui a proteção correta contra esse tipo de ataque.

Como vimos no curso, utilizamos um token próprio para impedir essa vulnerabilidade. chamado de CSRF Token. Ele consiste em uma série de caracteres aleatórios, gerados a cada formulário a ser preenchido pelo usuário que é enviado pelo servidor.

Após o recebimento pelo usuário, o token é checado novamente. O servidor só aceita o POST caso o CSRF Token se provar igual ao enviado inicialmente.

Diferentemente do session token e dos cookies, o CSRF Token não pode ser utilizado por um hacker mal intencionado.

Dessa forma, a existência do CSRF Token é crucial em todo formulário da web, para que o envio de formulários não seja forjado por terceiros.

Como já adicionamos as configurações necessárias para CSRF Token no **jogoteca.py** falta apenas adicionar nos formulários. Assim em **editar.html** abaixo da tag hidden
```
{{ form.csrf_token() }}
```
faça o mesmo para o **login.html** e para o **novo.html** e insira logo apos a tag fieldset.

aqui darei um commit "validando formulario e CSRF".


