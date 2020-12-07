FROM python:3.9

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app

# RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

COPY . /app

CMD python app.py