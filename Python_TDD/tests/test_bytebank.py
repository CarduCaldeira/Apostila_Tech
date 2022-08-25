from codigo.bytebank import Funcionario

class TestClass:
    def test_quando_idade_recebe_13_03_2000_deve_retornar_22(self):
        entrada = "13/03/2000" #Given-Contexto
        esperado = 22 

        funcionario_teste = Funcionario("Teste", entrada,1000)
        resultado = funcionario_teste.idade() # When - ação

        assert resultado == esperado # Then-desfecho

    def test_quando_sobrenome_recebe_Lucas_Carvalho_deve_retornar_Carvalho(self):
        entrada = "Lucas Carvalho" # Given
        esperado = "Carvalho"

        funcionario_teste = Funcionario(entrada,'11/11/2000',1000)
        resultado = funcionario_teste.sobrenome() # When 

        assert resultado == esperado # then

    def test_quando_decrescimo_salario_recebe_100000_deve_retornar_90000(self):
        entrada_salario = 100000 #Given
        entrada_nome = 'Paulo Bragança'
        esperado = 90000

        funcionario_teste = Funcionario(entrada_nome, '11/11/2000', entrada_salario)
        funcionario_teste.decrescimo_salario() # when
        resultado = funcionario_teste.salario

        assert resultado == esperado  # then

    



