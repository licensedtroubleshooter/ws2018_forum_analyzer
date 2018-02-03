# Forum Analyzer

[Описание](#%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5)

[Сборка](#%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0)


Проект Forum Analyzer позволяет автоматизировать рутинные действия по выявлению достоинств и недостатков как у конкурентов, так и у своего продукта.


## Описание

   ### Целевая аудитория: 
   
   Продуктовые аналитики.
   
   ### Решаемая проблема:
   
   Чтобы сделать свой продукт идеальным, предпринимателю необходимо прочитать и проанализировать множество отзывов потребителей, использовавших данный продукт от другого производителя.
   Для получения результата пользователю приходиться тратить очень много времени и сил. 
   Вышеуказанная проблема актуальна при анализе качества предоставления услуг разного рода. 
   Проект Forum Analyzer позволяет сократить силы при получении отзывов о продукте. 
   Результатом использования Forum Analyzer является список часто встречающихся слов и кластаризация всех комментариев. 
   Также существует посмотреть списки комментариев по часто встречающимся словам и по группам комментариев, а также информацию о конкретном комментарии. 

  Forum Analyzer предоставляется в виде web-сайта.

## Сборка

#### Требования

Необходимо предустановить python, pip, virtualenv, PostgreSQL (с dev-пакетом)

Для начала установим tkinker

```
sudo apt-get install python3-tk
```
Склонировать репозиторий на сервер

```
git clone <ws2018_forum_analyzer> (ссылка?)
```

Войти в папку 
```
cd ~/ws2018_forum_analyzer/venv
```

```
virtualenv -p python3 web
```

```
sourse ~/ws2018_forum_analyzer/venv/web/bin/activate
```
Устанавливаем пакеты python
```
pip scpy, numpy, pandas, vk, catboost, psycopg2, scikit-learn, gensim, nltk, pymystem3, django==1.11.7
```
Входим в командную строку python

```
python
```

Выполняем операции 

```
import nltk
nltk.download('stopworld')
exit()
```

Не знаю как написать 

```
cd ..
```

 ```
 python manage.py makemigration
 python manage.py makemigration text
 python manage.py makemigration tags
 python manage.py makemigratio makemigration clusters
 python manage.py migrate
 ```

