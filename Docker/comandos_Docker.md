# Tutorial Docker

Voltar à [Página inicial](README.md).

## Instalação 
Para instalar o docker no ubuntu siga o tutorial em <https://docs.docker.com/engine/install/ubuntu/>.

## Comandos Docker
Para listar as imagens contruídas 
``` 
docker images
```
Para listar os containers (inclusive os parados)
``` 
docker container ps -a
```
Para parar e apagar todos os containers 
``` 
docker stop $(docker container ps -aq)
docker rm  $(docker container ps -aq)
```
Para apagar apenas os containers parados 
``` 
docker container prune
```
Para apagar todas as imagens
``` 
docker rmi  $(docker images)
```
ou 
``` 
docker image prune -a
```
Para apagar apenas as imagens nao utilizadas (que não é associada a nenhum container em execução)
``` 
docker image prune 
```
## Como criar e executar uma imagem
Para criar uma imagem o docker utiliza um arquivo denominado Dockerfile, que define e descreve como uma imagem Docker deve ser construída. O comando para criar uma imagem
```
docker build -t <name-image> .
```
O "contexto" em Docker refere-se ao conjunto de arquivos e diretórios que são enviados para o daemon do Docker quando você executa o comando docker build. Por padrão, o contexto é o diretório atual em que você está quando executa o comando docker build. Para mudar o diretorio de contexto basta enviar como parametro o caminho do diretorio de contexto (o caminho será relativo ao diretorio de execução do docker build).
```
docker build -t minha-imagem:1.0 -f /caminho/para/meu/Dockerfile /caminho/do/novo/contexto
``` 
A tag -f determina em qual diretorio o docker ira procurar o Dockerfile.
Para executar uma imagem no modo interarivo adicione a tag -i, 
```
docker run -it <name-image> -p <porta-de-saida-do-host>:<porta-de-saida-do-container> network my-bridge  volume app-volume 
```
## Volumes

Como os containers são projetados para fornecer isolamento de recursos e  de ambientes para os aplicativos em execução dentro deles, ao encerrar a execução de um container por padrão não ha persistencia de dados. Para isso é necessário configurar um volume. Os dois principais modos de configurar um volume são denominados bind mount e named mount. O primeiro é realizada a persistencia por meio um diretorio local e o segundo o diretorio sera administrado pelo docker. Para o bind mount 
```
docker run -v /caminho/absoluto/no-host:/caminho/no-contêiner nome-da-imagem
```
ou para o caminho relativo
```
docker run -v ./caminho-relativo-no-host:/caminho/no-contêiner nome-da-imagem
```
Para o named volume basta referenciar o nome do volume (caso não exista o Docker ira cria-lo).
```
docker run -v nome-do-volume:/caminho/no-contêiner nome-da-imagem
```
Para criar um volume explicitamente 
```
docker volume create nome-do-volume
```
## Networks

No caso de rodarmos varios containers que precisam se comunicar entre si o Docker oferece a possibilidade de criar uma rede para a comunicação entre tais containers. Há três tipos de redes no docker, a host, none e bridge. A host utilizará a sua rede local, isto é, não haverá isolamento entre a rede do Docker e a local. A none seu container não terá acesso a nenhuma rede. A rede bridge é a padrão e ao contrario da host tera isolamento.
```
docker run --network minha-rede -p 8080:80 meu-webapp
```
Para criar a rede previamente
```
docker network create minha-rede
```
## Dockerfile
A seguir um exemplo de um dockerfile
```
ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:-compute,utility}

RUN apt update && \
    apt install -y \
        wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
        libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ARG PYTHON_VERSION

RUN cd /tmp && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make && make install && \
    cd .. && rm Python-${PYTHON_VERSION}.tgz && rm -r Python-${PYTHON_VERSION} && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip && \
    python -m pip install --upgrade pip && \
    rm -r /root/.cache/pip

ARG PYTORCH_VERSION
ARG PYTORCH_VERSION_SUFFIX
ARG TORCHVISION_VERSION
ARG TORCHVISION_VERSION_SUFFIX
ARG TORCHAUDIO_VERSION
ARG TORCHAUDIO_VERSION_SUFFIX
ARG PYTORCH_DOWNLOAD_URL

RUN if [ ! $TORCHAUDIO_VERSION ]; \
    then \
        TORCHAUDIO=; \
    else \
        TORCHAUDIO=torchaudio==${TORCHAUDIO_VERSION}${TORCHAUDIO_VERSION_SUFFIX}; \
    fi && \
    if [ ! $PYTORCH_DOWNLOAD_URL ]; \
    then \
        pip install \
            torch==${PYTORCH_VERSION}${PYTORCH_VERSION_SUFFIX} \
            torchvision==${TORCHVISION_VERSION}${TORCHVISION_VERSION_SUFFIX} \
            ${TORCHAUDIO}; \
    else \
        pip install \
            torch==${PYTORCH_VERSION}${PYTORCH_VERSION_SUFFIX} \
            torchvision==${TORCHVISION_VERSION}${TORCHVISION_VERSION_SUFFIX} \
            ${TORCHAUDIO} \
            -f ${PYTORCH_DOWNLOAD_URL}; \
    fi && \
    rm -r /root/.cache/pip

WORKDIR /workspace
```
As variaveis de ambiente ARG são variaveis que são utilizadas durante o build da imagem, nao existindo apos sua construção (util por exemplo caso use algum token que pode comprometer a segurança) enquanto ENV permanece como uma variavel de ambiente na imagem.

## Docker-compose

Como executar todos esses comandos ao executar uma imagem pode ser muito verboso e repetitivo, a melhor opçao é configurar um docker compose.
```
version: '3'

services:
  web:
    build: 
      context: ./all-service
      dockerfile: ./service-B/Dockerfile      # Usa um Dockerfile no diretório "meu-app"
    volumes:
      - app-data:/app/data  # Monta um volume nomeado chamado "app-data" no contêiner
    networks:
      - minha-rede          # Usa a rede personalizada "minha-rede"
    ports:
      - "8080:80"           # Mapeia a porta 8080 do host para a porta 80 do contêiner

networks:
  minha-rede:               # Define uma rede personalizada chamada "minha-rede"
    driver: bridge

volumes:
  app-data:                 # Define um volume nomeado chamado "app-data"

```
```
packages/button
├── lib
│   ├── button.d.ts
│   ├── button.js
│   ├── button.js.map
│   ├── button.stories.d.ts
│   ├── button.stories.js
│   ├── button.stories.js.map
│   ├── index.d.ts
│   ├── index.js
│   └── index.js.map
├── package.json
├── src
│   ├── button.stories.tsx
│   ├── button.tsx
│   └── index.ts
└── tsconfig.json
```
### Pincipais comandos Docker-Compose
Para construir uma imagem a partir do docker-compose.yml
```
docker-compose build
```
Para executar (e construir caso precise) uma imagem a partir do docker-compose.yml
```
docker compose up 
``` 
Para encerrar a execução da imagem
``` 
docker-compose down
``` 
Para mostrar informaçoes e logs 
```
docker-compose ps
docker-compose logs
```

## Dockerignore


