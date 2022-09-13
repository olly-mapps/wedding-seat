FROM python:3.10

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

WORKDIR .

ENTRYPOINT ["python"]

CMD ["main.py"]