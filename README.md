## 📚 Visão Geral

Este projeto simula a integração entre o CMMS **TracOS** e um **ERP de cliente**, O objetivo do projeto é **importar ordens de serviço (workorders)** fornecidas por um ERP no formato JSON, traduzi-las para o padrão do TracOS, persistir no banco, e exportar de volta as ordens processadas.  

Todo o fluxo é dividido em dois serviços principais:

- 🔁 **InboundService**: lê arquivos JSON que simulam a entrada do ERP, valida e transforma os dados, e os persite no MongoDB.
- 📤 **OutboundService**: busca os registros ainda não sincronizados e exporta de volta no formato original do cliente.

## 🧱 Arquitetura

A estrutura do projeto foi pensada para ser **modular, extensível e fácil de manter**, utilizando princípios como **SOLID**, tipagem forte com **Pydantic** e validações com **mypy**.


## 🚀 Subindo o projeto

### 1. Clone o repositório

```
git clone https://github.com/ErickAlmeida702/tractian_integrations_engineering_technical_test
cd tractian_integrations_engineering_technical_test
```

### 2. Crie o ambiente virtual com Poetry

```
poetry install
```

### 3. Suba o MongoDB com Docker

```
sudo docker-compose up -d
```

---

### 4. Configurando  variaveis de ambiente**  
   ```bash  
   # Create a .env file or export directly in your shell  
   echo "MONGO_URI=mongodb://localhost:27017/tractian" > .env   echo "DATA_INBOUND_DIR=./data/inbound" >> .env   echo "DATA_OUTBOUND_DIR=./data/outbound" >> .env  
   ```

## 📂 Estrutura esperada

- Os arquivos de entrada (inbound) devem estar no diretório `inbound/`
    
- Os arquivos exportados (outbound) aparecerão em `outbound/`
    

---

## 🏁 Executando o projeto

Dentro do ambiente virtual do Poetry:

```
poetry run python -m src.main
```

Esse comando irá:

- Processar todos os arquivos `.json` encontrados em `inbound/`
    
- Armazenar os dados no MongoDB
    
- Exportar registros sincronizados para o diretório `outbound/`
    

---

## 🧪 Executando os testes

```
poetry run pytest
```

## 📌 Melhorias Futuras

-  Substituir persistência mock por MongoDB real com conexão via API
    
-  Usar Kafka para orquestrar mensagens entre sistemas

    Melhorar o uso da Docker