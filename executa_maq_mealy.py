#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from maq_mealy import maq_mealy
import os.path

diretorio_maquinas = "maquinas/"
diretorio_imagens = "imagens/"

opcao_sim = ['s', 'S', 'sim', 'y', 'yes']
    
print """
Máquina de Mealy

Digite 0 (zero) para que os dados sejam lidos do arquivo ou 
1 (um) para que sejam adicionados via teclado."""

opcao = int(raw_input("0 ou 1? "))
while opcao not in [0, 1]:
    print "Opcao invalida, digite novamente. "
    opcao = int(raw_input("0 ou 1? "))

if opcao == 0:
    nome_arquivo = raw_input("Digite o nome do arquivo: maquinas/")
    
    # checando se o arquivo de configuracao passado existe
    while not os.path.isfile(diretorio_maquinas + nome_arquivo):
        print "O arquivo \"%s\" não existe! Digite novamente." % (nome_arquivo)
        nome_arquivo = raw_input("Digite o nome do arquivo: " + diretorio_maquinas)
        
    # instancia a maquina de mealy passando um dicionario como parametro pro construtor da classe
    m = maq_mealy(file=diretorio_maquinas + nome_arquivo)

elif opcao == 1:
    config = {}
    config['nome'] = raw_input("Nome da Máquina de Mealy: ")
    config['tipo'] = 'mealy'
    config['informacoes'] = "Máquina de Mealy de testes"
    config['num_estados'] = int(raw_input("Número de estados: "))
    config['alfabeto_entrada'] = []
    config['alfabeto_saida'] = []
    config['estados_finais'] = []    
    config['transicoes'] = []
            
    num_alfabeto_entrada = int(raw_input("Quantidade de caracteres do alfabeto de entrada: "))
    num_alfabeto_saida = int(raw_input("Quantidade de caracteres do alfabeto de saida: "))
    num_estados_finais = int(raw_input("Quantidade de estados finais: "))
    num_transicoes = num_alfabeto_entrada * config['num_estados']
    
    for i in range(num_alfabeto_entrada):
        config['alfabeto_entrada'].append(raw_input("Caractere de entrada %s: " % str(i + 1)))

    for i in range(num_alfabeto_saida):
        config['alfabeto_saida'].append(raw_input("Caractere de saida %s: " % str(i + 1)))

    for i in range(num_estados_finais):
        config['estados_finais'].append(raw_input("Estado finais (maximo %d): " % int(config['num_estados']-1)))
    
    config['estado_inicial'] = int(raw_input("Estado inicial: "))
        
    print "Transições:"
    for i in range(num_transicoes):
        print "\n=> Transição %d" % i
        estado = int(raw_input("Número do estado: "))
        leitura = raw_input("Quando lê: ")
        proximo = int(raw_input("Vai para o estado: "))
        saida = raw_input("E escreve: ")
        
        # adiciona a transicao na matriz de transicoes
        config['transicoes'].append( [estado, leitura, proximo, saida] )
        
    # instancia a maquina de mealy passando um dicionario como parametro pro construtor da classe    
    m = maq_mealy(config=config)

# fim da entrada de dados

# imprime informacoes na maquina de mealy    
info = m.get_info()
print '\nNome: %s' % (info['nome'])
print 'Descrição: %s' % (info['info'])

# recebe uma string que sera a entrada da maquina de mealy e a executa
w = raw_input("\nString de entrada: ")
m.executa(w)

# se a validacao da maquina de turing obteve sucesso, mostra passo a passo e outras opções

if m.sucesso():
    print "\nPasso a passo:"
    print m.get_pap()

    print "Entrada : %s" % m.get_entrada()
    print "Output  : %s" % m.get_output()

    if m.aceita():
        print "\n => A string foi aceita. A máquina parou no estado final q%d e percorreu toda a entrada.\n" % m.get_estado_atual()
    else:
        print "\n => A string foi rejeitada. Parou no estado q%d e na posição %d (de %d) da entrada.\n" % (m.get_estado_atual(), m.get_posicao(), len(m.get_entrada()))

    #
    # opcoes de gravar em arquivo e salvar imagem PNG da maquina (utilizando graphviz)
    #
    
    opcao_gravar = raw_input("Deseja salvar a máquina de mealy em um arquivo? (s/n) ")
    if opcao_gravar in opcao_sim:
        arquivo_out = raw_input("Nome do arquivo de saída: " + diretorio_maquinas)
        
        if os.path.isfile(diretorio_maquinas + arquivo_out):
            confirma = raw_input("O arquivo já existe, deseja sobrescreve-lo? (s/n) ")
            if confirma in opcao_sim:
                m.gravar_arquivo(diretorio_maquinas + arquivo_out)
        else:
            m.gravar_arquivo(diretorio_maquinas + arquivo_out)

    opcao_gravar = raw_input("Deseja salvar uma representação (PNG) da máquina de mealy? (s/n) ")
    if opcao_gravar in opcao_sim:
        arquivo_out = raw_input("Nome do arquivo de saída (ex: mealy): " + diretorio_imagens )
        
        if os.path.isfile(diretorio_imagens + arquivo_out):
            confirma = raw_input("O arquivo já existe, deseja sobrescreve-lo? (s/n) ")
            if confirma in opcao_sim:
                m.gravar_imagem(diretorio_imagens + arquivo_out)
        else:
            m.gravar_imagem(diretorio_imagens + arquivo_out)

        print "\nExecute o comando abaixo para gerar a imagem da máquina de mealy (na pasta de imagens):"
        print "$ dot -T png -o %s.png %s.dot && rm %s.dot" % (diretorio_imagens + arquivo_out, diretorio_imagens + arquivo_out, diretorio_imagens + arquivo_out)
        
        
# se a validacao da maquina de mealy não obteve sucesso, mostra o erro
        
else:
    print m.get_erro()

