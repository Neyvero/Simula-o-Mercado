
# Simula-Mercado-Digital

## Descrição do projeto

<img src="./examplo.jpg"/>

Este código utiliza conceitos de estruturas de dados para realizar uma simulação de mercado, com funções de carrinhos e compras automatizadas, incluindo histórico do carrinho realizada por busca binária e utilizando conceitos como FIFO e LIFO.

O projeto conta com módulos como CustomTkinter, JSON, os, e messagebox.

---

## Instruções de execução

Após baixar o arquivo `.zip` e descompactar, siga os passos abaixo:

### Ativar ambiente virtual (Windows PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

Caso ocorra algum erro, faça:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py --version
py -m venv .venv
.\.venv\Scripts\activate
```

### Instalação das dependências

```bash
pip install django
pip install django-bootstrap-v5
pip install djangorestframework mysqlclient
pip install djangorestframework
pip install pymysql
```

### Rodar o projeto

```bash
python manage.py runserver
```

---

## Tecnologias utilizadas

- Python 3.12  
- Django  
- Django REST Framework  
- Django Bootstrap 5  
- MySQL  
- CustomTkinter  
- pymysql
- JavaScript

---

## Estrutura dos arquivos

```
Simula-Mercado-Digital/
├── .venv/
├── mercado/
  ├──/__pycache__/
  ├──/migrations/
  ├──/static/mercado/ style.css
  ├──/templates/mercado/ index.html
├── Projeto/
├── users/         
├── manage.py               
```

---

## Configurações adicionais

- Instale o MySQL: https://dev.mysql.com/downloads/installer/  
- Instale o XAMPP e inicie o MySQL nele.  
- No MySQL, configure o usuário root sem senha (padrão).  
- Crie o banco de dados com o comando SQL:

```sql
CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

- Verifique se a porta MySQL no XAMPP está ativa e configurada corretamente.

---

## Integrantes do grupo

| Nome                    |
|-------------------------|
| Neyverson               |
| Ythalo                  |
| Henrique                |
| Caio Proença            |
| Gustavo Henrique Fragoso|
| Ícaro                   |
| Yuri                    | 
| Davi                    |
