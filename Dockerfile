FROM python:3.6.9
ADD main.py     .
ADD secret.py   . 

RUN pip3 install Flask Flask-SQLAlchemy Flask-MySQLdb requests PyMySQL  

CMD ["python3", "./main.py"]
