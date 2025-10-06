# Projeto AdotaTech 


O AdotaTech é uma plataforma web dinâmica desenvolvida para centralizar e otimizar a gestão de abrigos de animais, ONGs e protetores independentes. A aplicação tem como objetivo principal combater o problema do abandono e maus-tratos de animais, facilitando a conexão entre a comunidade e os animais que aguardam por um lar. Visão Geral do Projeto Muitas cidades brasileiras enfrentam um grande desafio com o descontrole populacional de animais de rua. Os abrigos, embora essenciais, frequentemente carecem de ferramentas digitais eficientes para gerenciar doações, atrair voluntários e dar visibilidade aos animais disponíveis para adoção. O AdotaTech surge como a solução para este problema, oferecendo uma interface intuitiva e um sistema de gerenciamento completo.
Desenvolvido com Python, FastAPI, HTML, JAVASCRIPT, CSS, SQLite

- em construção 

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