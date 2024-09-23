# Asyncio

Asyncio é uma biblioteca padrão do Python que fornece uma infraestrutura completa para escrever código assíncrono. Ele permite a criação, execução e gestão de corrotinas, bem como de outros tipos de tarefas assíncronas (como Tasks e Futures). Asyncio fornece um loop de eventos, que é o núcleo do seu sistema assíncrono, e gerencia a execução das tarefas assíncronas.

Uso: asyncio é usado para lidar com I/O assíncrono, como operações de rede, leitura/gravação de arquivos, e qualquer outro tipo de tarefa que possa se beneficiar de uma execução não bloqueante. Com asyncio, você pode esperar (await) por corrotinas, agendar tarefas, lidar com exceções assíncronas e coordenar tarefas complexas que exigem paralelismo cooperativo.

## Funcionalidades

- [Tasks](#tasks)
- [Gather](#gather)
- [GroupTasks](#grouptasks)
- [Futures](#futures)
- [Lock](#lock)
- [Events](#events)
- [Condition](#condition)

## Corrotinas 

Corrotinas são uma forma mais generalizada de sub-rotinas. Sub-rotinas tem a entrada iniciada em um ponto, e a saída em outro ponto. Corrotinas podem entrar, sair, e continuar em muitos pontos diferentes. Elas podem ser implementadas com a instrução async def. No exemplo abaixo mostra como executar uma corrotina.

```
>>> import asyncio

>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')

>>> asyncio.run(main())
```
Perceba que apenas chamar a corrotina não irá agendá-la para ser executada:
```
>>> main()
<coroutine object main at 0x1053bb7c8>
```

## Tasks

As Tasks são um modo de agendar a execução de uma corrotina. Uma Task é um objeto que é associado a uma corrotina e é executado em um loop de eventos. Para realmente executar uma corrotina, o asyncio fornece três mecanismos principais:

- A função asyncio.run() para executar a função “main()” do ponto de entrada no nível mais alto (veja o exemplo acima.)

- Aguardando uma corrotina (await). O seguinte trecho de código exibirá “hello” após esperar por 1 segundo e, em seguida, exibirá “world” após esperar por outros 2 segundos:

```
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```
Resultado esperado:
```
started at 17:13:52
hello
world
finished at 17:13:55
```
- A função asyncio.create_task():

```
async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")
```

Perceba que a saída esperada agora mostra que o trecho de código é executado 1 segundo mais rápido do que antes (porque as duas corrotinas say_after são executadas concorrentemente):

```
started at 17:14:32
hello
world
finished at 17:14:34
```

Enquanto são executas as tarefas task1 e task2 (idealmente estas tarefas devem ser do tipo I/O, como por exemplo download/exclusão de arquivos ou requisições) podemos executar uma função de um calculo, no await será aguardado a conclusão das tasks.

```
task1 = asyncio.create_task(
        say_after(1, 'hello'))

task2 = asyncio.create_task(
    say_after(2, 'world'))


execute_math_operation()

await task1
await task2

```

## Gather

Pra executar múltiplas corrotinas concorrentemente existe o método `asyncio.gather()`. 

```
import asyncio

async def fetch_data(id, sleep_time):
    
    print(f"Coroutine {id} starting to fetch data")
    await asyncio.sleep(sleep_time)
    return {"id":id, "data": f"Sample data from coroutine {id}"}

async def main():
    
    results = await asyncio.gather(fetch_data(1,2), fetch_data(2,1), fetch_data(3,3))

    for result in results:
        print(f"Received result: {result})

asyncio.run(main())
```

No caso de um lista de corrotinas basta usar o desempacotamento

```
tasks = [download_data(url) for url in urls]

results = await asyncio.gather(*tasks)
```

## GroupTasks

O TaskGroup é uma adição ao módulo asyncio do Python, introduzida no Python 3.11. Ele facilita o gerenciamento de múltiplas tarefas (tasks) assíncronas ao permitir que você agrupe essas tarefas em um único contexto.

- Gerenciamento de Tarefas Simples: Com o TaskGroup, você pode iniciar e gerenciar várias tarefas assíncronas dentro de um bloco with. Todas as tarefas iniciadas dentro desse bloco são monitoradas pelo TaskGroup.

- Encerramento Automático: Quando o bloco with termina, o TaskGroup automaticamente espera que todas as tarefas sejam concluídas. Se alguma tarefa falhar, o TaskGroup lida com isso e pode cancelar as demais tarefas se necessário.

- Erros Tratados Juntos: Se uma ou mais tarefas dentro de um TaskGroup falharem, o erro pode ser capturado de maneira centralizada e todas as tarefas não finalizadas serão canceladas.

```
try:
	# create a taskgroup
	async with asyncio.TaskGroup() as group:
		task1 = group.create_task(coro1())
		task2 = group.create_task(coro2())
		task3 = group.create_task(coro3())

	# wait for all group tasks are done
except:
	# all non-done tasks are cancelled
	pass
```

## Futures

Futures são objetos que representam um resultado que estará disponível em algum ponto no futuro. Quando uma future é concluída, ela pode fornecer um resultado ou lançar uma exceção se algo deu errado durante a operação.

```
import asyncio

async def load_configuration(future):
    print("Loading configuration...")
    await asyncio.sleep(2)  # Simulates reading a configuration file
    configuration = {"url": "http://example.com", "timeout": 5}
    future.set_result(configuration)  # Sets the result of the Future

async def use_configuration(name, future):
    print(f"{name} waiting for the configuration...")
    configuration = await future  # Waits for the Future to be completed
    print(f"{name} using the configuration: {configuration['url']} with a timeout of {configuration['timeout']} seconds.")

async def main():
    future_configuration = asyncio.Future()
    
    # Load the configuration in the background
    asyncio.create_task(load_configuration(future_configuration))
    
    # Multiple coroutines wait for the configuration
    await asyncio.gather(
        use_configuration("Task 1", future_configuration),
        use_configuration("Task 2", future_configuration),
        use_configuration("Task 3", future_configuration)
    )

asyncio.run(main())
```
Neste exemplo o await future retorna o resultado de future.set_result().


## Lock

No caso de haver uma variável que é compartilhada em diferentes corrotinas, ou alguma operação no banco de dados, a execução concorrente pode trazer resultados inesperados. Para garantir a consistência nesses casos o asyncio disponibiliza o  `asyncio.Lock`, que verifica se alguma tarefa esta executando o código dentro de async with lock e bloqueia a execução desse pedaço de código em outras tarefas, sendo necessário a finalização da tarefa atual nesse pedaço pra desbloquea-ló,

```
import asyncio

contador = 0
lock = asyncio.Lock()

async def incrementa():
    global contador
    for _ in range(100000):
        async with lock:
            contador += 1

async def main():
    tarefas = [incrementa() for _ in range(10)]
    await asyncio.gather(*tarefas)

asyncio.run(main())
print(f"Contador final: {contador}")
```

No caso anterior sem o Lock o valor final esperado poderia ficar menor que o esperado já que poderia haver valores "perdidos" devido à interferência entre as corrotinas.

## Semaphore

Ao contrário do Lock que so permite a execução de uma tarefa dentro do seu contexto podemos ter a necessidade de termos n tarefas executando determinado código ao mesmo tempo, como por exemplo um bloco de código que executa requisições e por limitação da API podemos ter que limitar o número de requisições. 

```
import asyncio

semaphore = asyncio.Semaphore(3)

async def tarefa(id):
    async with semaphore:
        print(f"Corrotina {id} adquirida")
        await asyncio.sleep(2)  
        print(f"Corrotina {id} liberada")

async def main():

    tarefas = [tarefa(i) for i in range(10)]
    await asyncio.gather(*tarefas)

asyncio.run(main())
```
Nesse exemplo até três tarefas podem adquirir o semaphore ao mesmo tempo.

## Events

Um objeto Event gerencia uma flag interna que pode ser definida como true com o método set() e redefinida como false com o método clear(). O método wait() bloqueia até que a flag seja definida como true. A flag é definido como false inicialmente.

```
async def waiter(event):

    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()

    # Wait until the waiter task is finished.
    await waiter_task

asyncio.run(main())
```

## Condition

Para situações mais complexas o asyncio disponibiliza o asyncio.Condition que pode ser usado por uma tarefa para esperar que algum evento aconteça e então obter acesso exclusivo a um recurso compartilhado.

Em essência, um objeto Condition combina a funcionalidade de um Event e um Lock. É possível ter vários objetos Condition compartilhando um Lock, o que permite coordenar o acesso exclusivo a um recurso compartilhado entre diferentes tarefas interessadas em estados particulares desse recurso compartilhado.
