#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ##############################################################################
# Trabalho de Teoria da Computação
# Simulador de Máquina de Mealy
# Copyright, 2010 por Luis Henrique B. Sousa, Lucas L. Garcia
#
# Arquivo maq_mealy.py
# -> Implementação do core da Máquina de Mealy (funções e classe)
#
# Código licenciado sob a GNU GPL versão 2.0 ou superior
#
# Versão: 1.0 novembro de 2010
# ###############################################################################

import ConfigParser
import os.path

class maq_mealy:
    
    """
    Esta classe implementa uma máquina de Mealy. 
    Retorna uma saída (output) que é feita em cada transição (e não nos estados,
    como nas Máquinas de Moore)
    
    @param o arquivo de configuração
    @param dicionário de configuração
    """
    
    def __init__(self, file=None, config={}):
        
        """
        Método construtor da classe. É um tipo de construtor múltiplo,
        pois pode receber um arquivo de configuração ou um dicionário.
        """
        
        # se a instancia passou um arquivo como parametro
        
        if file:
            if os.path.isfile(file):
                self.__le_arquivo(file)
            else:
                return
        
        # senão, a instancia passou um dicionário de configuração
            
        elif len(config) > 0:
            self.nome             = config['nome']
            self.tipo             = config['tipo']
            self.informacoes      = config['informacoes']
            self.qte_estados      = config['num_estados']
            self.alfabeto_entrada = config['alfabeto_entrada']
            self.alfabeto_saida   = config['alfabeto_saida']
            self.estados_finais   = config['estados_finais']
            self.estado_inicial   = config['estado_inicial']
            self.transicoes       = config['transicoes']
        
        # não passou nenhum dos dois
        
        else:
            return
        
        # inicializa atributos
        
        self.erro      = None
        self.est_atual = 0
        self.cabeca    = 0
        self.posicao   = 0
        self.estados   = []
        self.entrada   = ""
        self.output    = ""
        self.pap       = ""


    def __le_arquivo(self, conf):
        
        """
        Recupera informações do arquivo de configuração da máquina de Mealy.
        Diferente da MT padrão, as máquinas de Mealy não tem estado(s) final(is).    
        """
        
        config = ConfigParser.RawConfigParser()
        config.read(conf)

        self.tipo = config.get('dados_gerais', 'tipo')
        self.nome = config.get('dados_gerais', 'nome')
        self.informacoes = config.get('dados_gerais', 'informacoes')
        
        self.qte_estados = int(config.get('dados_maquina', 'qte_estados'))
        
        self.alfabeto_entrada = eval(config.get('dados_maquina', 'alfabeto_entrada'))
        self.alfabeto_saida = eval(config.get('dados_maquina', 'alfabeto_saida'))
        self.estados_finais = eval(config.get('dados_maquina', 'estados_finais'))
        self.estado_inicial = eval(config.get('dados_maquina', 'estado_inicial'))
                
        self.transicoes = eval(config.get('dados_maquina','transicoes'))


    def gravar_arquivo(self, arquivo):
    
        """
        Salva a máquina de mealy em um arquivo de configurações.
        """
        
        config = ConfigParser.RawConfigParser()
        config.add_section('dados_gerais')
        config.add_section('dados_maquina')
        
        config.set('dados_gerais', 'tipo', self.tipo)
        config.set('dados_gerais', 'nome', self.nome)
        config.set('dados_gerais', 'informacoes', self.informacoes)
        
        config.set('dados_maquina', 'qte_estados', self.qte_estados)
        config.set('dados_maquina', 'alfabeto_entrada', self.alfabeto_entrada)
        config.set('dados_maquina', 'alfabeto_saida', self.alfabeto_saida)
        config.set('dados_maquina', 'estados_finais', self.estados_finais)
        config.set('dados_maquina', 'estado_inicial', self.estado_inicial)
        config.set('dados_maquina', 'transicoes', self.transicoes)
               
        with open(arquivo, 'wb') as configfile:
            config.write(configfile)


    def validar_maquina(self):
        
        """
        Uma máquina de mealy é válida se não tem não-determinismo e se os caracteres de entrada
        e saída condizem, respectivamente, com os alfabetos de entrada e saída.
        """
        
        valida = True
        
        if not self.__confere_num_transicoes():
            valida = False

        elif not self.__confere_alfabeto_entrada(self.entrada, self.alfabeto_entrada):
            valida = False
            
        elif not self.__confere_alfabeto_saida(self.entrada, self.alfabeto_saida):
            valida = False
    
        elif not self.__confere_num_estados(self.qte_estados):
            valida = False
  
        elif not self.confere_nao_determinismo():
            valida = False        
        
        return valida
        
        
    def __confere_num_transicoes(self):
    
        """
        Método para conferir se o número de transições está correto. Está incorreto quando
        há o número de transições é maior do que o produto dos estados e da quantidade de
        caracteres do alfabeto de entrada.
        """
    
        if len(self.transicoes) > self.qte_estados * len(self.alfabeto_entrada):
            self.erro = "ERRO: O número de transições está incorreto."
            return False

        else:
            return True


    def __confere_alfabeto_entrada(self, fita, alfabeto):
    
        """
        Método para conferir se todos os caracteres na string de entrada pertencem
        ao alfabeto definido. Se algum caractere não faça parte do alfabeto, uma
        mensagem de erro é definida nos atributos de passo a passo e final, e false
        é retornado. Caso contrário, a conferência obteve sucesso e retorna true.
        """
        
        for c in fita:
            if not c in alfabeto:
                self.erro = "ERRO: O caractere %s não faz parte do alfabeto de entrada." % c
        
        for t in self.transicoes:
            entrada = t[1]
            if not entrada in alfabeto:
                self.erro = "ERRO: O caractere %s não faz parte do alfabeto de entrada." % entrada

        if self.erro:
            return False
        
        return True
        
        
    def __confere_alfabeto_saida(self, fita, alfabeto):
    
        """
        Método para conferir se todos os caracteres na string de saida pertencem
        ao alfabeto definido. Se algum caractere não faça parte do alfabeto, uma
        mensagem de erro é definida nos atributos de passo a passo e final, e false
        é retornado. Caso contrário, a conferência obteve sucesso e retorna true.
        """
        
        for t in self.transicoes:
            saida = t[3]
            for c in saida:
                if not c in alfabeto:
                    self.erro = "ERRO: O caractere %s não faz parte do alfabeto de saída." % saida

        if self.erro:
            return False
        
        return True        
        
        
    def __confere_num_estados(self, qtd_estados):
    
        """
        Método para conferir se o número de estados é consistente com os estados colocados
        nas transições.
        """
              
        for t in self.transicoes:
            if t[0] not in self.estados:
                self.estados.append(t[0])
        
        if len(self.estados) <= qtd_estados:
            return True
            
        else:
            self.erro = "O número de estados está incorreto."    
            return False


    def confere_nao_determinismo(self):
    
        """
        Checa se um estado tem mais de uma transição possível quando lê um entrada.
        """
        
        k = 0
        cont = 0
        
        while k < len(self.transicoes) and cont < 2 and not self.erro:
            estado  = self.transicoes[k][0]
            leitura = self.transicoes[k][1]
                       
            for transicao in self.transicoes:
                if transicao[0] == estado and transicao[1] == leitura:
                    cont += 1
                    
                if cont > 1:
                    self.erro = "ERRO: Uma Máquina de Mealy não pode ter não-determinismo."

            cont = 0
            k += 1
        
        return self.erro == None


    def executa(self, fita, *args):
        
        """
        Método principal da máquina, pois processa a string na máquina de Mealy e produz uma saída (output).
        """

        self.entrada = fita
        
        if len(args) == 0:       
            
            if not self.validar_maquina():
                return

            self.est_atual = 0
            
            # variavel de controle sobre as transicoes
            
            t = 0
            
            for caractere in self.entrada:
                
                continua = True
                                               
                while continua and (t < len(self.transicoes)):
    
                    self.cabeca = caractere   

                    estado  = self.transicoes[t][0]
                    leitura = self.transicoes[t][1]
                    proximo = self.transicoes[t][2]
                    escrita = self.transicoes[t][3]
                    
                    if self.cabeca == leitura and self.est_atual == estado:
                        self.output = self.output.replace('_', '') + "_" + escrita
                        self.pap += "(q%d: %3s / %5s)  => output: %s\n" % (estado, self.cabeca, escrita, self.output)
                        self.est_atual = proximo
                        continua = False
                        self.posicao += 1
                        
                        if t <= len(self.transicoes):
                            t = 0
                        
                    else:
                        t += 1
                                                    
            return self.output
    
    def aceita(self):
        if (self.est_atual in self.estados_finais) and (self.posicao >= len(self.entrada)):
            return True
        else:
            return False
    
    def get_output(self):
        return self.output.replace('_', '')
     
    def get_entrada(self):
        return self.entrada 
    
    def get_pap(self):
        return self.pap
        
    def sucesso(self):
        return self.erro == None
        
    def get_erro(self):
        return self.erro
    
    def get_info(self):
        return { 'tipo': self.tipo, 'nome': self.nome, 'info': self.informacoes }

    def get_estado_atual(self):
        return self.est_atual

    def get_posicao(self):
        return self.posicao
        
    def gerar_imagem(self):
    
        """
        Utilizando o aplicativo graphviz.org, geramos um arquivo com informações da máquina de mealy.
        A imagem é gerada usando o comando: $ dot -T png -o maq_mealy.png maq_mealy.dot
        """
    
        states = self.estados
        states.sort()
        
        qfs = " ".join(map(str, self.estados_finais))

        dot_graph = 'digraph mealy_machine {\n'
        dot_graph += '    rankdir=LR;\n'
        dot_graph += '    edge [fontname=arial,fontsize=11]\n'
        dot_graph += '    node [shape=circle,size=8]\n'
        dot_graph += '    start [shape=point]\n'
        dot_graph += '    start -> %s\n' % self.estado_inicial
        dot_graph += '    node [fontname=arial,fontsize=11,shape=doublecircle]\n'
        dot_graph += '    '  + qfs
        dot_graph += ';\n'
        dot_graph += '    node [shape=circle,size=8]\n'

        for state in range(len(self.transicoes)):
            values = self.transicoes[state]
            dot_graph += '    %s -> %s [label="%s/%s"]\n' % (values[0], values[2], values[1], values[3])

        dot_graph += '}\n'

        return dot_graph        
        
    def gravar_imagem(self, nome_arquivo="imagens/maq_mealy.png"):
    
        """
        Cria código de um arquivo do aplicativo graphviz.org para depois gerar uma imagem da máquina.
        """
        
        try:
            dotfile = file(nome_arquivo + ".dot", "wb")
            dotfile.write(self.gerar_imagem())
        except IOError:
            pass
        
        
