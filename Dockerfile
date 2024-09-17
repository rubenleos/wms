FROM python:3.12.5
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3","-m","flask","--app", "app","run","--host=0.0.0.0"] 