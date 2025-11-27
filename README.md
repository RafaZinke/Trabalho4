# Sistema de Cotação de Fretes

# Desenvolvido por: Rafael Zink

# &nbsp;GitHub: https://github.com/RafaZinke/Trabalho4

# 

# Objetivo

# Sistema de cotação de fretes que demonstra a aplicação prática de Design Patterns orientados a objetos no domínio de logística.

# Padrões Implementados

# Padrão

# Aplicação

# Benefício

# Strategy

# Cálculo de frete (zona/peso/volume/expresso)

# Trocar algoritmo dinamicamente

# Decorator

# Serviços adicionais (pedágios/seguro/embalagem)

# Compor funcionalidades

# Factory Method

# Criação de transportadoras por SLA

# Criar objetos de forma modular

# Singleton

# Configuração e Log centralizados

# Instância única no sistema

# 

# Problema Resolvido

# Empresas de logística precisam:

# Calcular fretes com diferentes critérios (zona, peso, volume)

# Adicionar serviços opcionais de forma flexível

# Escolher transportadoras com diferentes prazos e preços

# Manter configurações e logs centralizados

# 

# &nbsp;Como Executar

# Pré-requisitos

# python --version  # Requer Python 3.8+

# Executar Sistema

# python main.py

# O menu permite:

# Cotar Entrega - Simular uma cotação completa

# Ver Logs - Histórico de operações

# Sair

# Exemplo de Uso

# &nbsp;MENU PRINCIPAL

# 1\. Cotar Entrega

# &nbsp;Escolha: 1

# 

# Origem: São Paulo

# Destino: Rio de Janeiro

# Zona: regional

# Peso: 10 kg

# Volume: 0.5 m³

# 

# Estratégia: 1 (Por Zona)

# SLA: 2 (Padrão - 5 dias)

# Serviços: pedagio,seguro

# 

# Resultado: R$ 106.34 | ExpressLog Padrão | 5 dias

# 

# &nbsp;Como Testar

# Executar Testes

# python test\_main.py

# &nbsp;

# Linguagem: Python 3.8+ |

# 

