FROM python:3.9.19-alpine3.18

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=service.py

# CMD ["flask", "run"]

CMD ["python3", "service.py"]
