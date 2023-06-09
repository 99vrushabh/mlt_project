FROM python:3.8-slim-buster

WORKDIR /py-docker  
#its create a directory in the container where all this files are saved 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
# here two dots means at start which file was saved it will never changed in that build
#first dot shows current directory will copy in the current work dirctory

EXPOSE 3000

ADD app.py .

RUN export FLASK_APP=app.py

CMD ["flask","run", "--host", "0.0.0.0", "--port", "5000"]
    