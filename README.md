# Projeto AdotaTech 

Este é um projeto de backend para um sistema de adoção de animais, desenvolvido com FastAPI e Python.

O objetivo principal deste repositório é demonstrar a manipulação de um banco de dados **SQLite** utilizando **SQL puro**

## Como Executar

1. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   ```
   ```bash
   source venv/bin/activate  # No Linux/Mac
   .\venv\Scripts\activate    # No Windows
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o servidor:**
   ```bash
   uvicorn main:app --reload
   ```
   Ao iniciar, o servidor criará automaticamente o arquivo de banco de dados `adotatech.db` com as tabelas necessárias.

4. **Acesse a documentação da API:**
   Abra seu navegador e vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).