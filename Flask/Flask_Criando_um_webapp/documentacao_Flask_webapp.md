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

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def ola():
    return render_template('lista.html')

app.run()

Darei um commit com nome "primeiro webapp".


