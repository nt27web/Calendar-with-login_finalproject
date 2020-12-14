FROM python:3

#set envionment variables
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

WORKDIR /app

RUN pip install --upgrade pip

copy requirements.txt .

RUN pip install -r requirements.txt

COPY app /app

CMD python login_controller.py
#CMD python rest_app.py