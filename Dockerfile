FROM python:3

#set envionment variables
ENV PYTHONUNBUFFERED 1

EXPOSE 5000
# RUN pip install --upgrade pip

WORKDIR /
copy requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
copy app /app
CMD python login_controller.py
# & calendar_controller.py
