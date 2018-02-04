# Forum Analyzer

![Иллюстрация работы системы](https://pp.userapi.com/c621701/v621701448/67627/Acmb3WoArHc.jpg)![Иллюстрация работы системы](https://pp.userapi.com/c621701/v621701858/610fe/fTU5HCKE98s.jpg)

Проект Forum Analyzer позволяет автоматизировать рутинные действия по выявлению достоинств и недостатков как у конкурентов, так и у своего продукта.

## Содержание

[Описание](#%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5)

[Сборка](#%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0)

[Функциональная спецификация]()


## Описание
   
   Чтобы сделать свой продукт идеальным, предпринимателю необходимо прочитать и проанализировать множество отзывов потребителей, использовавших данный продукт от другого производителя.
   Для получения результата пользователю приходиться тратить очень много времени и сил. 
   Вышеуказанная проблема актуальна при анализе качества предоставления услуг разного рода. 
   Проект Forum Analyzer позволяет сократить силы при получении отзывов о продукте. 
   Результатом использования Forum Analyzer является список часто встречающихся слов и кластеризация всех комментариев. 
   Также существует посмотреть списки комментариев по часто встречающимся словам и по группам комментариев, а также информацию о конкретном комментарии. 

  Forum Analyzer предоставляется в виде web-сайта.
  
![Схема](https://pp.userapi.com/c621701/v621701448/67616/WmwrKo0EdB8.jpg)  

## Сборка

#### Требования:

Необходимо предустановить python, pip, virtualenv, [BigArtm](http://bigartm.org), PostgreSQL (с dev-пакетом)

#### Установка:

Для начала необходимо установить tkinker:

```bash
sudo apt-get install python3-tk
```

Клонировать репозиторий:

```bash
git clone https://github.com/42lacksky/ws2018_forum_analyzer.git
```

Создать и активировать виртуальное окружение: 

```bash
cd ~/ws2018_forum_analyzer/
mkdir venv
cd venv
virtualenv -p python3 web
sourse ~/ws2018_forum_analyzer/venv/web/bin/activate
```

Установить в виртуальное окружение пакеты python:

```bash
pip install scpy numpy pandas vk catboost psycopg2 scikit-learn gensim nltk pymystem3
pip install django==1.11.7 (если планируете использовать web-интерфейс)
```

Выполнить команды: 

```bash
python
>>> import nltk
>>> nltk.download('stopwords')
>>> exit()
```

Выполнить команды:

 ```bash
 python <путь>/ws2018_forum_analyzer/manage.py makemigration
 python <путь>/ws2018_forum_analyzer/manage.py makemigration text
 python <путь>/ws2018_forum_analyzer/manage.py makemigration tags
 python <путь>/ws2018_forum_analyzer/manage.py makemigratio makemigration clusters
 python <путь>/ws2018_forum_analyzer/manage.py migrate
 ```
 
#### Проверить работоспособность установленного приложения:

Web-интерфейс:

```bash
python <путь>/ws2018_forum_analyzer/manage.py runserver <адрес:порт>
```
По умолчанию используется localhost:8000

Исключительно алгоритм: 

```bash
python
>>> import src
>>> import src.datadase
>>> import forum_analyze\
>>> src.datadase.add_group_to_postgres('<ссылка на ГРУППУ в вк>')
```

## Функциональная спецификация

[Ссылка](https://docs.google.com/document/d/18uVuXm7miM2IqS7I25g-lZsa3oHjvFOMgkOiS1TfwD8/edit?ts=5a7302eb#)
