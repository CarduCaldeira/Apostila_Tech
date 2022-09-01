# Flask: webapp

Voltar à [Página inicial](../../README.md).

Neste markdown irei documentar o curso "MLOps: Machine Learning e APIs" da Alura enquanto realizo ele.

O projeto em que serão aplicados os conceitos estão nesta pasta Machine_Learning_Flask.md. 

Para não nos perdemos entre as modificações no projeto e esta documentação, todo commmit dado será reportado aqui. A ideia é que tal documento siga o curso de forma linear.

## Primeiros passos

Instale um ambiente virtual 
```
python3 -m venv ./venv
```
Para ativar 
```
source /home/carlos/Documentos/Apostila_Tech/Apostila_Tech/MLOps/Machine_Learning_Flask/venv/bin/activate
```
Aqui darei um commit "primeiros passos MLOps Flask".

## Integrando um modelo de Machine Learning

Crie um arquivo **main.py** e nele crie uma api padrão. 
```
from flask import Flask
from textblob import TextBlob #biblioteca de analise de sentimento

app = Flask(__name__)

@app.route('/')
def home():
    return "Minha primeira Api"

app.run(debug=True)
```
Na rota abaixo iremos implementar um código  que faz uma análise de sentimento (quanto mais próximo de 1 mais positiva e quanto mais próxima de -1 mais negativa) da frase inserida na url
'http://127.0.0.1:5000/sentimento/frase'
```
@app.route('/sentimento/<frase>')
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt',to='en')
    polaridade = tb_en.sentiment.polarity
    return 'polaridade:{}'.format(polaridade)
```
Vamos implementar um algoritmo de regressão linear para prever os valores de casas. Note que para só precisamos treinar o modelo uma vez, portanto não devemos colocá-lo dentro do endpoint, pois todas vez que acessarmos o endpoint o modelo será treinado. Adicione ao **main.py** 
```
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv('casas.csv')
colunas = ['tamanho','preco']
df = df[colunas]

X = df.drop('preco',axis =1)
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo = LinearRegression()
modelo.fit(X_train, y_train)
```
E crie o seguinte endpoint 
```
@app.route('/cotacao/<int:tamanho>')
def cotacao(tamanho):
    preco = modelo.predict([[tamanho]])
    return str(preco)
```
Por exemplo, se informarmos 120 para o modelo (inserindo http://127.0.0.1:5000/cotacao/120)
temos como reposta [157377.06185642]. Podemos visualizar o coefiente angular deste modelo de regressão com o comando
```
modelo.coef_
```
e o linear com
```
modelo.intercept_
```
Note porém que para o nosso modelo estamos enviando apenas um dado, caso quissesemos treinar tal modelo com tamanho, ano e garagem (e portanto teríamos que enviar três dados) como faríamos? Além nossa saída é um array, mas também não poderíamos enviar como um json?
Alterando o código nesse sentido ele deve ficar 
```
from flask import Flask, request, jsonify
from textblob import TextBlob #biblioteca de analise de sentimento
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv('casas.csv')
colunas = ['tamanho','ano','garagem']


X = df.drop('preco',axis =1)
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo = LinearRegression()
modelo.fit(X_train, y_train)

app = Flask(__name__)

@app.route('/')
def home():
    return "Minha primeira Api"

@app.route('/sentimento/<frase>')
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt',to='en')
    polaridade = tb_en.sentiment.polarity
    return 'polaridade:{}'.format(polaridade)

@app.route('/cotacao/', methods=['POST'])
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True)
```
Note que o comando 
```
dados_input = [dados[col] for col in colunas]
```
serve para enviar os dados para o modelo na ordem correta, indepedente da order que o usuario informar o json.

Aqui darei um commit "precificando casas no Flask".
