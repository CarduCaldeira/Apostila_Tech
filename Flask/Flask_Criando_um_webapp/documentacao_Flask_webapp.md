# Flask: webapp

Voltar à [Página inicial](../../README.md).

Neste markdown irei documentar o curso "Flask: criando um webapp" da Alura enquanto realizo ele.

O projeto em que serão aplicados os conceitos estão nesta pasta Flask_Criando_um_webapp. 

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
source /home/carlos/Documentos/Apostila_Tech/Apostila_Tech/Python_TDD/venv/bin/activate
```
Para instalar os requirementos rode
```
pip3 install -r requirements.txt 
```

Aqui darei o primeiro commit com nome "primeiros passos para Flask: webapp".

## Criando a primeira pagina

Cire um arquivo jogoteca.py e insira
```
from flask import Flask

app = Flask(__name__)

@app.route('/inicio')
def ola():
    return '<h1>Olá Mundo!</h1>'

app.run()
```
Rodando esse arquivo já temos a nossa primeira pagina em http://127.0.0.1:5000/inicio. Por enquanto 
nossa pagina apenas mostra a mensagem "Olá mundo", como podemos renderizar um código html mais elaborado? Crie uma pasta com nome templates, e dentro um arquivo lista.html com o seguinte código
```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Jogoteca</title>
  </head>
  <body>
    <div class="container">
        <div class="page-header">
            <h1>{{ titulo }}</h1>
        </div>
        <table class="table table-striped table-responsive table-bordered">
            <thead class="thead-default">
                <tr>
                    <th>Nome</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>God of War</td>
                </tr>
                <tr>
                    <td>Skyrim</td>
                </tr>
                <tr>
                    <td>Valorant</td>
                </tr>
            </tbody>
        </table>
    </div>
  </body>
</html>
```
Para conseguirmos renderizar tal código devemos importar a biblioteca "render_template" e 
dar "return render_template('lista.html')"
```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def ola():
    return render_template('lista.html')

app.run()
```

Darei um commit com nome "primeiro webapp".

## Conteúdos dinâmicos

Substitua  em **lista.html** o código "<title>Jogoteca</title>" por  "<title>{{ titulo }}</title>"
e em **jogoteca.py**  deixe da seguinte forma:
```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def ola():
    return render_template('lista.html', titulo='Jogos')

app.run()
```
Note agora que o título da nossa pagina http://127.0.0.1:5000/inicio é 'Jogos'. No próximo passo deixaremos nossa página ainda mais dinâmica.

Agora deixe o arquivo **jogoteca.py** da seguinte forma
```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def ola():
    lista = ['Tetris', 'Skyrim', 'Crash']
    return render_template('lista.html', titulo='Jogos', jogos=lista)

app.run()
```

E **lista.html** substitua 
```
    <tbody>
        <tr>
            <td>God of War</td>
        </tr>
        <tr>
            <td>Skyrim</td>
        </tr>
        <tr>
            <td>Valorant</td>
        </tr>
    </tbody>
```
Por 
```
 <tbody>
{% for jogo in jogos %}    
                <tr>
                    <td>{{ jogo }}</td>
                </tr>
{% endfor %}
</tbody>
```
Note então que estamos mostrando a lista '['Tetris', 'Skyrim', 'Crash']' dinamicamente. Vamos utilizar
orientação a objetos agora. Crie a classe **Jogo** e instacie três objetos que serão enviados para o lista.html por meio de uma lista, como abaixo: 

```
from flask import Flask, render_template

app = Flask(__name__)

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

@app.route('/inicio')
def ola():
    jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
    jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
    jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
    lista = [jogo1, jogo2, jogo3]
    return render_template('lista.html', titulo='Jogos', jogos=lista)

app.run()
```
Em **lista.html**  substitua 
```
<thead class="thead-default">
    <tr>
        <th>Nome</th>
    </tr>
</thead>
<tbody>
    {% for jogo in jogos %}    
                    <tr>
                        <td>{{ jogo }}</td>
                    </tr>
    {% endfor %}
</tbody>
```
por
```
<thead>
    <tr>
        <th>Nome</th>
        <th>Categoria</th>
        <th>Console</th>
    </tr>
</thead>
<tbody>
{% for jogo in jogos %}    
                <tr>
                    <td>{{ jogo.nome }}</td>
                    <td>{{ jogo.categoria }}</td>
                    <td>{{ jogo.console }}</td>
                </tr>
{% endfor %}
</tbody>
```

Aqui darei um novo commit com o nome "conteúdo dinâmico".

## Formulários

Imagine agora que queremos cadastrar novos jogos por meio de um formulário. Para isso crie um arquivo 
**novo.html** em **templates** e insira:
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Jogoteca</title>
</head>
<body>
    <div class="container">
      <div class="page-header">
          <h1>{{ titulo }}</h1>
      </div> 
      <form>
        <fieldset>
          <div class="form-group">
            <label for="nome">Nome</label>
            <input type="text" id="nome" name="nome" class="form-control">
          </div>
          <div class="form-group">
            <label for="categoria">Categoria</label>
            <input type="text" id="categoria" name="categoria" class="form-control">
          </div>
          <div class="form-group">
            <label for="console">Console</label>
            <input type="text" id="console" name="console" class="form-control">
          </div>
          <button type="submit" class="btn btn-primary btn-salvar">Salvar</button>
        </fieldset>
      </form>
    </div>
</body>
</html>
```

Vamos criar uma rota para esta página. Assim, em **jogoteca.py** insira
```
@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')
app.run()
```
Note que já podemos ver a página http://127.0.0.1:5000/novo, porém quando inserimos os dados no formulário continuamos na mesma pagina e além disso os dados informados são mostrados na url da página
(não queremos esse comportamento, imagine se estamos informando um dado sigiloso). Então em **novo.html** e substitua 
```
<form >
```
por 
```
<form action="/criar" method="post">
```
Note que somos direcionados para a página http://127.0.0.1:5000/criar, que não apresenta nada.
Queremos que quando inserirmos os dados no formulário sejamos direcionados para a página http://127.0.0.1:5000/inicio e ela já mostre os dados que inserimos. Para isso, em **jogoteca.py** insira 
```
@app.route('/criar')
def criar():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
```
e da library **flask import  request**. Também retire a criação da lista de dentro do escopo da função ola e coloque ela de forma que tal lista seja global. Como tal lista agora é global conseguimos acessá-la em **criar**. Assim em **criar** adicione 
```
lista.append(jogo)
return render_template('lista.html', titulo='Jogo', jogos=lista)
```
O arquivo **jogoteca.py** deve ficar dessa forma
```
from flask import Flask, render_template, request

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

app = Flask(__name__)

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

@app.route('/inicio')
def ola():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar')
def criar():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return render_template('lista.html', titulo='Jogo', jogos=lista)

app.run()
```
Observe que se reiniciarmos a aplicação ela apresentará uma erro. Para corrigir isto devemos substituir
```
@app.route('/criar')
```
por

```
@app.route('/criar', methods=['POST',])
```
pois por padrão o flask só aceita requisições GET. Mude **app.run()** para **app.run(debug=True)** e renomeie a função ola para index e altere sua rota para /. Reinicie o app, a partir de agora toda vez que altermarmos o nosso projeto o flask irá restaurar automaticamente. Perceba que a página esta funcionado agora, porém ainda ao cadastrar um novo jogo continuamos na pagina criar(que deve ser apenas uma página de meio termo). Assim substitua 
```
return render_template('lista.html', titulo='Jogo', jogos=lista)
```
por
```
return redirect('/')
```
E devemos importar o **redirect** no topo do código.

Aqui daremos mais um commit com nome "criando formulário".







    
