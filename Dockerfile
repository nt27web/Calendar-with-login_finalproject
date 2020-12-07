FROM python:3

#set envionment variables
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

RUN pip install --upgrade pip
#COPY requirements.txt /app
#ADD requirements.txt /app/
RUN pip install -r requirements.txt

COPY app /app
CMD python app.py