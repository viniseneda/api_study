FROM python:3.9.19-alpine3.18

WORKDIR /code

RUN pip3 install flask pymongo

COPY . .

ENV FLASK_APP=service.py

# CMD ["flask", "run"]

CMD ["python3", "service.py"]
