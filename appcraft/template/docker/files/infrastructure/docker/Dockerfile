FROM python:3.9-slim

WORKDIR /

COPY Pipfile Pipfile.lock /

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . /

CMD ["python", "run", "start"]
