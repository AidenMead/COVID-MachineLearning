FROM python:3.10
WORKDIR /api

RUN echo "Starting backend build..."

RUN pip install pipenv

COPY  . .

RUN pipenv install --system --deploy --ignore-pipfile

ENV FLASK_ENV production

CMD ["gunicorn", "--worker-class", "gevent", "-b", ":5001", "wsgi:app", "--timeout", "90"]