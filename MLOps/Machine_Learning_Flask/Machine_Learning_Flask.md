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

## Serializando nosso modelo

Podemos melhorar nosso projeto ao serializarmos nosso modelo. Imagine que temos um modelo robusto que demora minutos (ou até horas para treinar), além disso nossa base de dados é diaria, isto é, todo dia teremos que retreinar nosso modelo. Ao serializarmos nosso modelo a manutenção do nosso projeto fica mais pratica e eficiente.

Para isso crie um arquivo com nome **auxiliar.py** e coloque o código
```
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('casas.csv')

X = df.drop('preco',axis =1)
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# create an iterator object with write permission - model.pkl
with open('modelo.sav', 'wb') as files:
    pickle.dump(modelo, files)
```
ao rodá-lo, será criado um arquivo **modelo.sav** que transforma nosso modelo em binário.
Agora, podemos retirar de **main.py** o código
```
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('casas.csv')
X = df.drop('preco',axis =1)
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo = LinearRegression()
modelo.fit(X_train, y_train)
```
Para carregar o modelo insira no **main.py**
```
import pickle
modelo = pickle.load(open('modelo.sav','rb'))
```
Também podemos inserir uma autenticação nos endpoints. Para isso insira
```
from flask_basicauth import BasicAuth

app.config['BASIC_AUTH_USERNAME'] = 'carlos'
app.config['BASIC_AUTH_PASSWORD'] = '123'

basic_auth = BasicAuth(app)
```
E em cima do endpoint que deseja que tenha validação, insira 
```
@basic_auth.required
```
Ao final o código deve ficar
```
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob #biblioteca de analise de sentimento
from sklearn.linear_model import LinearRegression
import pickle

modelo = pickle.load(open('modelo.sav','rb'))
colunas = ['tamanho','ano','garagem']

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'carlos'
app.config['BASIC_AUTH_PASSWORD'] = '123'

basic_auth = BasicAuth(app)


@app.route('/')
def home():
    return "Minha primeira Api"

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt',to='en')
    polaridade = tb_en.sentiment.polarity
    return 'polaridade:{}'.format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True)
```
Agora vamos testar nossa aplicação.  Para isso criei o **request.ipynb** e basta rodá-lo.

Commit com nome "api de machine learning finalizada".