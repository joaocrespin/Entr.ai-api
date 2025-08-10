# Entr.ai API

Esta é a API desenvolvida em **Python**, como parte do projeto [**Entr.ai**](https://github.com/KenZohn/Entr.ai), realizado no **4º semestre da faculdade**. 

O Entr.ai é um sistema de controle de acesso para instituições, que utiliza reconhecimento facial para identificar pessoas autorizadas e liberar a entrada de forma automatizada.  
Foi desenvolvido em ambiente Linux, utilizando o ESP32 WROOM OV2640 + ESP32 MB para o reconhecimento facial, o ESP32 WROOM para o controle do portão e o SG90 como servo motor para abertura.

Esta API foi desenvolvida para realizar o controle básico do site do projeto, sendo responsável pela comunicação com o banco de dados, gerenciamento de usuários e registros de acesso.  
**Nota:** Esta versão da API **não é idêntica** à entregue no projeto final. A versão do projeto completo foi **adaptada** para atender melhor às necessidades específicas do Entr.ai.

---

## Tecnologias utilizadas

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Flask](https://img.shields.io/badge/FLASK-000000?style=for-the-badge&logo=flask&logoColor=white)
- ![SQLAlchemy](https://img.shields.io/badge/SQLALCHEMY-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white&logoSize=auto) 
- ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
- **pyttslib** 

---

## Como rodar o projeto

1. Clone o repositório:
  ```bash
   git clone https://github.com/joaocrespin/Entr.ai-api.git
   cd Entr.ai-api
  ```
2. Crie e ative um ambiente virtual:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

3. Instale as dependências:
  ```bash
  pip install -r requirements.txt
  ```
4. Execute a aplicação:
  ```bash
  flask run
  ```

## Endpoints


## TODO

- [ ] Documentar com o Swagger