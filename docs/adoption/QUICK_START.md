# Quick Start

## Introdução

Este guia apresenta os passos mínimos necessários para instalar e executar o Sistema de Monitoramento de Águas.

Tempo estimado:

5 a 10 minutos.

---

# Pré-Requisitos

Antes de iniciar, verifique se possui:

* Python 3.10 ou superior instalado;
* Git instalado;
* Sistema operacional Windows.

---

# Obter O Projeto

Clone o repositório:

```bash
git clone https://github.com/hendersonmauriciobatista-png/proteus.git
```

Acesse a pasta do projeto:

```bash
cd proteus
```

Troque para a branch principal de desenvolvimento:

```bash
git checkout feature/environment-data-v1
```

---

# Criar Ambiente Virtual

Windows:

```bash
python -m venv venv
```

Ativar:

```bash
venv\Scripts\activate
```

---

# Instalar Dependências

```bash
pip install -r requirements.txt
```

---

# Executar O Sistema

```bash
python main.py
```

A aplicação será iniciada em modo desktop.

---

# Primeiro Uso

Ao abrir o sistema você poderá navegar pelas seguintes áreas:

* Dashboard
* Painel Executivo
* Qualidade Da Água
* Dados Ambientais
* Consumo E Distribuição
* Relatórios
* Previsão Analítica
* Governança Operacional

---

# Fluxo Recomendado

Para uma primeira demonstração:

1. Registrar dados de qualidade da água.
2. Registrar dados ambientais.
3. Registrar consumo e distribuição.
4. Abrir Previsão Analítica.
5. Verificar Water Health Score.
6. Verificar alertas preventivos.
7. Abrir Governança Operacional.
8. Executar Sincronizar Alertas.
9. Abrir Painel Executivo.

---

# Solução De Problemas

## Erro: PyQt5 não encontrado

Instalar novamente:

```bash
pip install -r requirements.txt
```

---

## Ambiente virtual não ativado

Windows:

```bash
venv\Scripts\activate
```

---

## Aplicação não inicia

Verifique:

* versão do Python;
* instalação das dependências;
* existência do arquivo main.py.

---

# Observação

O Sistema de Monitoramento de Águas possui finalidade educacional, demonstrativa e de apoio observacional.

O sistema não substitui análises laboratoriais ou pareceres técnicos especializados.
